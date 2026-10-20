import sys
import time

from assistant_core.config import load_settings
from assistant_core.errors import AssistantError
from assistant_core.knowledge import Handbook, OfficeDirectory
from assistant_core.logging_setup import setup_logging
from assistant_core.models import Message
from assistant_core.service import AssistantService

logger = setup_logging()


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m assistant_core '<message>'")
        sys.exit(1)

    text = " ".join(sys.argv[1:])

    try:
        settings = load_settings()
        offices = OfficeDirectory.from_csv(settings.data_dir / "offices.csv")
        handbook = Handbook.from_json(settings.data_dir / "handbook.json")

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

    except AssistantError as err:
        logger.error(f"Error executing assistant: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()