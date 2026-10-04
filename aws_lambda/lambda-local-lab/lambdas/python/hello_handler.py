import logging
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info("Python Lambda received event: %s", event)

    return {
        "success": True,
        "message": "Hello from Python Lambda",
        "received_event": event,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }