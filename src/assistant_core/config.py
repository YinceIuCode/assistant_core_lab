import os

from assistant_core.errors import ConfigError
from dotenv import load_dotenv
from pydantic import BaseModel, Field


class Settings(BaseModel):    
    API_KEY : str | None = Field(default=None, repr=False)
    MODEL : str | None = "stub"
    RATE : int | None = 450000
    RETAKE_RATE : float | None = 1.5
    DEBUG : bool | None = True


def load_settings(env_file: str | None = ".env") -> Settings:
    if env_file:
        load_dotenv(env_file, override=False)
    
    s = Settings(
        API_KEY = os.getenv("API_KEY"),
        MODEL = os.getenv("MODEL"),
        RATE = int(os.getenv("RATE")) if os.getenv("RATE") is not None else None,
        RETAKE_RATE = float(os.getenv("RETAKE_RATE")) if os.getenv("RETAKE_RATE") is not None else None,
        DEBUG = None if os.getenv("DEBUG") is None else (False if os.getenv("DEBUG").lower() != "true" else True),
    )
    
    if s.MODEL != "stub" and not s.API_KEY:
        raise ConfigError(f"API_KEY is required when MODEL={s.MODEL!r}")
    return s