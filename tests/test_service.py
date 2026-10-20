from unittest.mock import MagicMock
import pytest

from assistant_core.errors import ProviderError
from assistant_core.models import Message, Intent
from assistant_core.service import AssistantService


class StubLLMResponder:
    def generate(self, message: Message):
        raise ProviderError("LLM responder failed")


def test_service_fallback_on_provider_error():
    settings = MagicMock()
    offices = MagicMock()
    handbook = MagicMock()

    service = AssistantService(settings, offices, handbook)
    
    service.responder = StubLLMResponder()

    msg = Message(text="test query")
    response = service.handle(msg)

    assert response.degraded is True