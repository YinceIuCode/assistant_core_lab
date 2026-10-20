from unittest.mock import MagicMock

from assistant_core.errors import ProviderError
from assistant_core.models import Message
from assistant_core.service import AssistantService


class StubLLMResponder:
    def explain(self, question: str, rule: object) -> str:
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