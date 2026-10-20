import pytest

from assistant_core.config import load_settings
from assistant_core.errors import ConfigError


def test_load_settings_defaults(monkeypatch):
    for var in ["API_KEY", "MODEL", "RATE", "RETAKE_RATE", "DEBUG"]:
        monkeypatch.delenv(var, raising=False)

    settings = load_settings(env_file=None)

    assert settings.MODEL == "stub"
    assert settings.RATE == 450000
    assert settings.RETAKE_RATE == 1.5
    assert settings.DEBUG is True


def test_load_settings_from_file():
    settings = load_settings(env_file=".env.example")

    assert settings.MODEL == "stub"
    assert settings.RATE == 450000
    assert settings.RETAKE_RATE == 1.5
    assert settings.DEBUG is True


def test_load_settings_bad(monkeypatch):
    monkeypatch.setenv("MODEL", "openai")
    monkeypatch.delenv("API_KEY", raising=False)

    with pytest.raises(ConfigError) as exc_info:
        load_settings(env_file=None)

    assert "API_KEY is required when MODEL='openai'" in str(exc_info.value)


def test_load_settings_with_custom_key(monkeypatch):
    monkeypatch.setenv("MODEL", "openai")
    monkeypatch.setenv("API_KEY", "sk-test-fake-key-123")

    settings = load_settings(env_file=None)

    assert settings.MODEL == "openai"
    assert settings.API_KEY == "sk-test-fake-key-123"