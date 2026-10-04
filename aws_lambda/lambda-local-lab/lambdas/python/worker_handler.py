import logging
import time
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info("Worker started. event=%s", event)

    try:
        # Simulate background work
        time.sleep(5)

        logger.info("Background work completed")

        return {
            "success": True,
            "message": "Python background task completed",
            "completed_at": datetime.now(timezone.utc).isoformat(),
        }

    except Exception:
        logger.exception("Worker failed")
        raise