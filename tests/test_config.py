from pathlib import Path

import pytest

from assistant_core.config import load_settings
from assistant_core.errors import ConfigError


def test_load_settings_defaults(monkeypatch):
    for var in [
        "ASSISTANT_DATA_DIR",
        "LLM_PROVIDER",
        "LLM_API_KEY",
        "CREDIT_RATE_VND",
        "RETAKE_MULTIPLIER",
        "MAX_CREDITS",
        "LOG_LEVEL",
    ]:
        monkeypatch.delenv(var, raising=False)

    settings = load_settings(env_file=None)

    assert settings.data_dir == Path("data")
    assert settings.llm_provider == "stub"
    assert settings.credit_rate_vnd == 450_000


def test_load_settings_from_file():
    settings = load_settings(env_file=".env.example")

    assert settings.data_dir == Path("data")
    assert settings.llm_provider == "stub"
    assert settings.credit_rate_vnd == 450_000
    assert settings.retake_multiplier == 1.5
    assert settings.max_credits == 30
    assert settings.log_level == "INFO"


def test_load_settings_bad(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.delenv("LLM_API_KEY", raising=False)

    with pytest.raises(ConfigError) as exc_info:
        load_settings(env_file=None)

    assert "LLM_API_KEY is required when LLM_PROVIDER='openai'" in str(exc_info.value)


def test_load_settings_with_custom_key(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("LLM_API_KEY", "sk-test-fake-key-123")

    settings = load_settings(env_file=None)

    assert settings.llm_provider == "openai"
    assert settings.llm_api_key == "sk-test-fake-key-123"
