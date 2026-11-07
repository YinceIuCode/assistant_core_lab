import hashlib
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def hash_session(raw_session: str, salt: str) -> str:
    return hashlib.sha256(f"{raw_session}{salt}".encode()).hexdigest()


class ChatSession(SQLModel, table=True):
    __tablename__ = "chat_session"
    id: str = Field(primary_key=True)
    channel: str = "web"
    created_at: datetime = Field(default_factory=utcnow)


class Interaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    request_id: str = Field(index=True, unique=True)
    session_id: str = Field(foreign_key="chat_session.id")
    intent: str
    topic: str | None = None
    resolved: bool = True
    degraded: bool = False
    latency_ms: float = 0.0
    created_at: datetime = Field(default_factory=utcnow)


class Feedback(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    request_id: str = Field(foreign_key="interaction.request_id")
    rating: int
    comment: str | None = None
    created_at: datetime = Field(default_factory=utcnow)


class IntentStat(SQLModel):
    intent: str
    requests: int
