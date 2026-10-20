import logging
import sys
import time
from pathlib import Path

from assistant_core.config import load_settings
from assistant_core.errors import AssistantError
from assistant_core.knowledge import Handbook, OfficeDirectory
from assistant_core.logging_setup import JsonFormatter
from assistant_core.models import Message
from assistant_core.service import AssistantService


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m assistant_core '<message>'")
        sys.exit(1)

    # Khởi tạo Logging chuẩn JSON
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonFormatter())
    logger = logging.getLogger("assistant_core")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    text = " ".join(sys.argv[1:])
    
    try:
        settings = load_settings()
        
        data_dir = Path("data")
        offices = OfficeDirectory.from_csv(data_dir / "offices.csv")
        handbook = Handbook.from_json(data_dir / "handbook.json")

        service = AssistantService(settings, offices, handbook)

        start_time = time.perf_counter()
        msg = Message(text=text)
        response = service.handle(msg)
        latency_ms = round((time.perf_counter() - start_time) * 1000, 1)

        logger.info(
            "handled",
            extra={
                "intent": response.intent.value if hasattr(response.intent, "value") else str(response.intent),
                "latency_ms": latency_ms,
                "session": msg.session_id,
                "degraded": response.degraded,
            },
        )

        print(response.answer)
        
    except AssistantError as e:
        logger.error(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()