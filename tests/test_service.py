from assistant_core.responder import StubLLMResponder

from assistant_core.config import Settings
from assistant_core.knowledge import Handbook, OfficeDirectory, Rule
from assistant_core.models import Message
from assistant_core.service import AssistantService


def test_service_greeting():
    settings = Settings()
    offices = OfficeDirectory({})
    handbook = Handbook([])
    service = AssistantService(settings, offices, handbook)

    res = service.handle(Message(text="hello"))
    assert "Hello!" in res.answer
    assert res.degraded is False


def test_fallback_when_provider_fails():
    settings = Settings()
    offices = OfficeDirectory({})
    handbook = Handbook([Rule(id="1", title="thesis registration credits", text="18 credits required.")])

    failing_responder = StubLLMResponder(fail=True)
    service = AssistantService(
        settings,
        offices,
        handbook,
        responder=failing_responder,
    )

    r = service.handle(Message(text="thesis registration credits"))
    assert r.degraded is True
    assert r.sources[0].id == "1"
    assert "18 credits required." in r.answer