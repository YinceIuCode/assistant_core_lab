import pytest

from assistant_core.errors import (
    AssistantError,
    ConfigError,
    DataError,
    InvalidRequest,
    ProviderError,
)


def test_exception_inheritance():
    assert issubclass(AssistantError, Exception)
    assert issubclass(ConfigError, AssistantError)
    assert issubclass(DataError, AssistantError)
    assert issubclass(InvalidRequest, AssistantError)
    assert issubclass(ProviderError, AssistantError)


@pytest.mark.parametrize(
    "error_class",
    [
        ConfigError,
        DataError,
        InvalidRequest,
        ProviderError,
    ],
)
def test_catch_specific(error_class):
    with pytest.raises(error_class) as exc_info:
        raise error_class("Test error message")

    assert "Test error message" in str(exc_info.value)


def test_catch_base_class():
    with pytest.raises(AssistantError):
        raise ConfigError("Config is broken")

    with pytest.raises(AssistantError):
        raise DataError("Data is missing")
