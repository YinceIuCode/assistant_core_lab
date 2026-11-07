import hashlib
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import case, func, event
from sqlalchemy.pool import StaticPool
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class ChatSession(SQLModel, table=True):
    __tablename__ = "chat_session"
    id: str = Field(primary_key=True, max_length=16)
    channel: str = Field(default="web", max_length=16)
    created_at: datetime = Field(default_factory=utcnow)
    interactions: list["Interaction"] = Relationship(back_populates="session")


class Interaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    request_id: str = Field(index=True, unique=True, max_length=32)
    session_id: str = Field(foreign_key="chat_session.id", index=True)
    intent: str = Field(index=True, max_length=16)
    topic: str | None = Field(default=None, max_length=32)
    resolved: bool = True
    degraded: bool = False
    latency_ms: float = 0.0
    created_at: datetime = Field(default_factory=utcnow, index=True)
    session: Optional["ChatSession"] = Relationship(back_populates="interactions")
    feedback: list["Feedback"] = Relationship(back_populates="interaction")


class Feedback(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    request_id: str = Field(foreign_key="interaction.request_id", index=True)
    rating: int
    comment: str | None = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=utcnow)
    interaction: Optional["Interaction"] = Relationship(back_populates="feedback")


def make_engine(db_url: str):
    connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}
    if db_url in ("sqlite://", "sqlite:///:memory:"):
        engine = create_engine(db_url, connect_args=connect_args, poolclass=StaticPool)
    else:
        engine = create_engine(db_url, connect_args=connect_args)

    if db_url.startswith("sqlite"):
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


def init_db(engine) -> None:
    SQLModel.metadata.create_all(engine)


def hash_session(raw: str, salt: str) -> str:
    return hashlib.sha256((salt + raw).encode()).hexdigest()[:16]


class Repository:
    def __init__(self, db_url_or_engine, salt: str = ""):
        if isinstance(db_url_or_engine, str):
            self.engine = make_engine(db_url_or_engine)
        else:
            self.engine = db_url_or_engine
        self.salt = salt

    def init_db(self) -> None:
        init_db(self.engine)

    def record_interaction(
        self,
        raw_session: str,
        request_id: str,
        intent: str,
        topic: str | None = None,
        resolved: bool = True,
        degraded: bool = False,
        latency_ms: float = 0.0,
    ) -> None:
        sid = hash_session(raw_session, self.salt)
        with Session(self.engine) as db:
            if db.get(ChatSession, sid) is None:
                db.add(ChatSession(id=sid))
            db.add(
                Interaction(
                    request_id=request_id,
                    session_id=sid,
                    intent=intent,
                    topic=topic,
                    resolved=resolved,
                    degraded=degraded,
                    latency_ms=latency_ms,
                )
            )
            db.commit()

    def add_feedback(self, request_id: str, rating: int, comment: str | None = None) -> Feedback | None:
        with Session(self.engine) as db:
            exists = db.exec(select(Interaction).where(Interaction.request_id == request_id)).first()
            if exists is None:
                return None
            fb = Feedback(request_id=request_id, rating=rating, comment=comment)
            db.add(fb)
            db.commit()
            db.refresh(fb)
            return fb

    def list_feedback(self, limit: int = 100) -> list[Feedback]:
        with Session(self.engine) as db:
            statement = select(Feedback).order_by(Feedback.created_at.desc()).limit(limit)
            return list(db.exec(statement).all())

    def intent_stats(self) -> list[dict]:
        with Session(self.engine) as db:
            resolved_cnt = func.sum(case((Interaction.resolved.is_(True), 1), else_=0))
            degraded_cnt = func.sum(case((Interaction.degraded.is_(True), 1), else_=0))
            
            q = (
                select(
                    Interaction.intent,
                    func.count().label("requests"),
                    resolved_cnt.label("resolved_count"),
                    degraded_cnt.label("degraded_count"),
                    func.avg(Interaction.latency_ms).label("avg_latency"),
                )
                .group_by(Interaction.intent)
                .order_by(func.count().desc())
            )
            rows = db.exec(q).all()

        return [
            {
                "intent": row[0],
                "requests": row[1],
                "resolved_count": int(row[2] or 0),
                "degraded_count": int(row[3] or 0),
                "avg_latency_ms": round(row[4] or 0.0, 1),
            }
            for row in rows
        ]