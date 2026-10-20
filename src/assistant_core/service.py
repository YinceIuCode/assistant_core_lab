import logging

from assistant_core.config import Settings
from assistant_core.errors import ProviderError
from assistant_core.knowledge import Handbook, OfficeDirectory
from assistant_core.models import Intent, Message, Response, Source
from assistant_core.responder import Responder, StubLLMResponder, TemplateResponder
from assistant_core.router import route
from assistant_core.tools import parse_credits, tuition

log = logging.getLogger("assistant_core")

class AssistantService:
    def __init__(
        self,
        settings: Settings,
        offices: OfficeDirectory,
        handbook: Handbook,
        responder: Responder | None = None,
    ):
        self.settings = settings
        self.offices = offices
        self.handbook = handbook
        self.responder = responder or StubLLMResponder()
        self.fallback = TemplateResponder()

    def handle(self, msg: Message) -> Response:
        intent = route(msg.text, self.offices.names)

        if intent is Intent.GREETING:
            return Response(
                answer="Hello! I can help with offices, fees and rules.",
                intent=intent,
            )

        if intent is Intent.FEE:
            return self._fee(msg.text)

        if intent is Intent.OFFICE:
            o = self.offices.find(msg.text)
            if o:
                return Response(
                    answer=f"{o.name.title()}: room {o.room}, open {o.hours}.",
                    intent=intent,
                )

        return self._rule(msg.text)

    def _fee(self, text: str) -> Response:
        credits, retake = parse_credits(text)
        cost = tuition(
            credits=credits,
            retake=retake,
            rate=self.settings.RATE,
            retake_multiplier=self.settings.RETAKE_RATE,
            max_credits=25
        )
        return Response(
            answer=f"Tuition fee: {cost:,} VND.",
            intent=Intent.FEE,
        )

    def _rule(self, text: str) -> Response:
        rule = self.handbook.search(text)
        if not rule:
            return Response(
                answer="I don't know.",
                intent=Intent.UNKNOWN,
            )
        
        sources = [Source(id=rule.id, title=rule.title)]
        
        try:
            answer = self.responder.explain(text, rule)
            return Response(
                answer=answer,
                intent=Intent.RULE,
                sources=sources,
            )
        except ProviderError:
            log.warning("provider failed; using template fallback")
            answer = self.fallback.explain(text, rule)
            return Response(
                answer=answer,
                intent=Intent.RULE,
                sources=sources,
                degraded=True,
            )