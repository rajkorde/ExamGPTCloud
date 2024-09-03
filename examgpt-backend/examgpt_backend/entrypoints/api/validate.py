import json
from typing import Any

from domain.model.utils.logging import app_logger

logger = app_logger.get_logger()


def handler(event: dict[Any, Any], context: Any) -> dict[str, Any]:
    logger.info("Executing validator.")
    logger.info(f"{event=}")

    # Get exam and validate state is at least chunked and not ready

    # Get chunks

    # Validate state of chunks

    # Get QA

    # print stats of chunks and QA

    # Set exam state to Ready

    # notify user that exam is ready

    return {
        "statusCode": 200,
        "body": json.dumps({"value": "test"}),
    }
