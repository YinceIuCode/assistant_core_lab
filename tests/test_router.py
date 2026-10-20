# tests/test_router.py
import pytest
from assistant_core.models import Intent
from assistant_core.router import route

def test_route_greeting():
    offices = {"library", "registrar"}
    assert route("Hello", offices) == Intent.GREETING

def test_route_fee():
    offices = {"library", "registrar"}
    assert route("tuition for 18 credits", offices) == Intent.FEE

def test_route_office():
    offices = {"library", "registrar"}
    assert route("where is the library", offices) == Intent.OFFICE

def test_route_rule():
    offices = {"library", "registrar"}
    assert route("can I register my thesis", offices) == Intent.RULE