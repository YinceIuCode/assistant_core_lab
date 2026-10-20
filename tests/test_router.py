import pytest

from assistant_core.models import Intent
from assistant_core.router import route


def test_route_greeting():
    offices = {"registrar", "admissions"}
    assert route("Hello!", offices) == Intent.GREETING
    assert route("  XIN CHAO? ", offices) == Intent.GREETING
    assert route("hi", offices) == Intent.GREETING


def test_route_fee():
    offices = {"registrar"}
    assert route("What is the tuition fee?", offices) == Intent.FEE
    assert route("how much is the fee payment?", offices) == Intent.FEE


def test_route_office():
    offices = {"registrar", "finance", "admissions"}
    assert route("Where is the registrar office?", offices) == Intent.OFFICE
    assert route("contact finance department", offices) == Intent.OFFICE


def test_route_rule_fallback():
    offices = {"registrar"}
    assert route("What are the graduation requirements?", offices) == Intent.RULE
    assert route("random unknown query string", offices) == Intent.RULE
