# router.py
from responder import TemplateResponder, StubLLMResponder

class Router:
    def __init__(self):
        self.template_responder = TemplateResponder()
        self.llm_responder = StubLLMResponder()
        self.history = []

    def route(self, query: str) -> str:
        if not query:
            return "empty"
        
        m = query.lower().strip()
        self.history.append(query)

        if m == "history":
            return "\n".join(self.history)
        
        # Thử phản hồi qua TemplateResponder trước
        resp = self.template_responder.generate_response(query)
        if resp != "Sorry I dont know":
            return resp

        # Nếu không khớp template, chuyển sang StubLLMResponder (tra cứu handbook/LLM)
        resp = self.llm_responder.generate_response(query)
        return resp

# Khởi tạo router mặc định để cung cấp hàm route() toàn cục theo yêu cầu
_default_router = Router()

def route(query: str) -> str:
    return _default_router.route(query)