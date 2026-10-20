import pytest

from assistant_core.errors import ProviderError
from assistant_core.responder import StubLLMResponder, TemplateResponder


class DummyRule:
    def __init__(self, title: str, text: str):
        self.title = title
        self.text = text

def test_template_responder():
    responder = TemplateResponder()
    rule = DummyRule(title="Thesis Registration", text="Submit your form before week 2.")
    
    result = responder.explain("how to register thesis?", rule)
    assert "Thesis Registration" in result
    assert "Submit your form" in result

def test_stub_llm_responder_success():
    responder = StubLLMResponder(fail=False)
    rule = DummyRule(title="Exam Rules", text="Bring your student ID.")
    
    result = responder.explain("what to bring to exam?", rule)
    assert "Exam Rules" in result

def test_stub_llm_responder_failure():
    responder = StubLLMResponder(fail=True)
    rule = DummyRule(title="Library", text="Quiet zone.")
    
    # Kiểm tra xem khi fail=True thì có bắn ra ProviderError đúng như yêu cầu không
    with pytest.raises(ProviderError):
        responder.explain("library rules", rule)