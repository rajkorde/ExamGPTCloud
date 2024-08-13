import json
import os
from typing import Any

from adapter.aws.content_service_s3 import ContentServiceS3
from domain.model.utils.logging import app_logger

CONTENT_SERVICE_TYPE = {"AWS": ContentServiceS3}
logger = app_logger.get_logger()


def get_error(
    message: str = "Something went wrong!", error_code: int = 500
) -> dict[str, Any]:
    return {
        "statusCode": error_code,
        "body": json.dumps(
            {
                "message": message,
            }
        ),
    }


def get_content_service():
    location = os.getenv("LOCATION")
    if not location:
        logger.error("No Environment Variable found: LOCATION")
        return None
    return CONTENT_SERVICE_TYPE[location]()
