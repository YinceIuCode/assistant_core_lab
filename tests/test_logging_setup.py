import json
import logging

from assistant_core.logging_setup import JsonFormatter


def test_json_formatter_basic():
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test_logger",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="test message",
        args=(),
        exc_info=None,
    )
    
    result = formatter.format(record)
    data = json.loads(result)
    
    assert data["level"] == "INFO"
    assert data["logger"] == "test_logger"
    assert data["msg"] == "test message"
    assert "intent" not in data

def test_json_formatter_with_extras():
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test_logger",
        level=logging.WARNING,
        pathname="",
        lineno=0,
        msg="test message with extra",
        args=(),
        exc_info=None,
    )
    
    # Gắn thêm các thuộc tính extra
    record.intent = "fee"
    record.latency_ms = 12.5
    record.session = "local_123"
    record.degraded = True
    
    result = formatter.format(record)
    data = json.loads(result)
    
    assert data["level"] == "WARNING"
    assert data["intent"] == "fee"
    assert data["latency_ms"] == 12.5
    assert data["session"] == "local_123"
    assert data["degraded"] is True