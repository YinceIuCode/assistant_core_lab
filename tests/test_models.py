import pytest
from pydantic import ValidationError

from assistant_core.models import Intent, Message, Response


def test_message_valid():
    msg = Message(text="where is the library?")
    assert msg.text == "where is the library?"
    assert msg.session_id == "local"

def test_message_invalid_empty():
    with pytest.raises(ValidationError):
        Message(text="")  # Sẽ báo lỗi vì models.py quy định min_length=1

def test_response_creation():
    resp = Response(answer="I.101", intent=Intent.OFFICE)
    assert resp.answer == "I.101"
    assert resp.intent == Intent.OFFICE
    assert len(resp.sources) == 0
    assert resp.degraded is False