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
    offices.names = set()  # Tránh lỗi vòng lặp ở router
    
    handbook = MagicMock()
    # Tạo một rule giả có chứa chuỗi thật để vượt qua ải Pydantic
    mock_rule = MagicMock()
    mock_rule.id = "rule_1"
    mock_rule.title = "Dummy Rule"
    handbook.search.return_value = mock_rule

    service = AssistantService(settings, offices, handbook)
    service.responder = StubLLMResponder()

    msg = Message(text="test query")
    response = service.handle(msg)

    assert response.degraded is True