"""FastAPI application — Lab 4 STARTER.  Run:  uvicorn assistant_api.main:create_app --factory --reload

Most of the file is given. Complete the four TODOs (T1–T4); the tests in tests/test_api.py tell you when you are done.

Endpoints (v1): GET /health, POST /v1/chat, POST /v1/feedback, GET /v1/feedback (admin), GET /v1/weather
"""

from __future__ import annotations

import uuid
from time import perf_counter

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from assistant_api.db import Repository
from assistant_api.ratelimit import RateLimiter
from assistant_api.schemas import (
    ChatRequest,
    ChatResponse,
    ErrorResponse,
    FeedbackIn,
    FeedbackOut,
    IntentStat,
    OfficeOut,
    Weather,
)
from assistant_api.weather import ExternalServiceError, WeatherClient
from assistant_core import AssistantService, Message, build_service
from assistant_core.config import Settings, load_settings


def create_app(
    settings: Settings | None = None,
    service: AssistantService | None = None,
    weather: WeatherClient | None = None,
    repo: Repository | None = None,
) -> FastAPI:
    settings = settings or load_settings()
    service = service or build_service(settings)
    weather = weather or WeatherClient(
        settings.weather_url, settings.campus_lat, settings.campus_lon, timeout_s=settings.weather_timeout_s
    )
    repo = repo or Repository(settings.database_url, settings.session_salt)
    repo.init_db()
    limiter = RateLimiter(settings.rate_limit_per_min)  # used only in the BONUS task

    app = FastAPI(
        title="Study Assistant API", version="1.0.0", description="Backend of the CSC10014 Smart Virtual Assistant."
    )

    def error(code: int, key: str, message: str) -> JSONResponse:
        return JSONResponse(status_code=code, content={"error": {"code": key, "message": message}})

    @app.exception_handler(RequestValidationError)
    async def on_validation(_: Request, exc: RequestValidationError):
        first = exc.errors()[0]
        field = ".".join(str(p) for p in first["loc"][1:]) or "body"
        return error(422, "invalid_request", f"{field}: {first['msg']}")

    @app.exception_handler(HTTPException)
    async def on_http(_: Request, exc: HTTPException):
        return error(exc.status_code, str(exc.detail).lower().replace(" ", "_"), str(exc.detail))

    def require_admin(x_api_key: str | None = Header(default=None)) -> None:
        if not settings.api_admin_key or x_api_key != settings.api_admin_key:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing or invalid API key")

    @app.get("/health", tags=["ops"])
    def health() -> dict:
        return {"status": "ok", "version": app.version}

    @app.post(
        "/v1/chat",
        response_model=ChatResponse,
        tags=["chat"],
        responses={422: {"model": ErrorResponse}, 429: {"model": ErrorResponse}},
    )
    def chat(req: ChatRequest, request: Request) -> ChatResponse:
        client = request.client.host if request.client else "unknown"
        if not limiter.allow(client):
            raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Too many requests")
        started_at = perf_counter()
        resp = service.handle(Message(text=req.message, session_id=req.session_id))
        request_id = uuid.uuid4().hex[:12]
        topic = resp.sources[0].id if resp.sources else None
        repo.record_interaction(
            req.session_id,
            request_id,
            resp.intent.value,
            topic=topic,
            resolved=resp.intent.value != "unknown",
            degraded=resp.degraded,
            latency_ms=(perf_counter() - started_at) * 1000,
        )
        return ChatResponse(**resp.model_dump(), request_id=request_id)

    @app.post("/v1/feedback", response_model=FeedbackOut, status_code=201, tags=["feedback"])
    def add_feedback(fb: FeedbackIn) -> FeedbackOut:
        item = repo.add_feedback(fb.request_id, fb.rating, fb.comment)
        if item is None:
            raise HTTPException(status_code=404, detail="Unknown request_id")
        return FeedbackOut.model_validate(item, from_attributes=True)

    @app.get("/v1/feedback", response_model=list[FeedbackOut], tags=["feedback"], dependencies=[Depends(require_admin)])
    def list_feedback(limit: int = Query(default=100, ge=1, le=100)) -> list[FeedbackOut]:
        """Retrieve all recorded feedback (Admin only)."""
        return [FeedbackOut.model_validate(item, from_attributes=True) for item in repo.list_feedback(limit=limit)]

    @app.get(
        "/v1/stats/intents",
        response_model=list[IntentStat],
        tags=["stats"],
        dependencies=[Depends(require_admin)],
    )
    def intent_stats() -> list[IntentStat]:
        return [IntentStat.model_validate(item) for item in repo.intent_stats()]

    @app.get("/v1/weather", response_model=Weather, tags=["external"], responses={503: {"model": ErrorResponse}})
    def campus_weather() -> Weather:
        # TODO: T4 (4 lines): call weather.current() inside try/except.
        #   If ExternalServiceError happens, raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE,
        #   "Weather service unavailable") from None
        try:
            return weather.current()
        except ExternalServiceError:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "weather service unavailable") from None

    @app.get("/v1/offices", response_model=list[OfficeOut], tags=["knowledge"])
    def all_offices() -> list[OfficeOut]:
        return [OfficeOut(name=office.name, room=office.room, hours=office.hours) for office in service.offices.all()]

    return app
