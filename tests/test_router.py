# tests/test_router.py
import pytest
from router import route

def test_route_empty():
    assert route("") == "empty"

def test_route_greeting():
    response = route("hi")
    assert "Hello" in response

def test_route_tuition():
    response = route("tuition for 10 credits")
    assert "Your tuition is" in response

def test_route_history():
    route("hi")
    route("hello")
    history_resp = route("history")
    assert "hi" in history_resp
    assert "hello" in history_resp