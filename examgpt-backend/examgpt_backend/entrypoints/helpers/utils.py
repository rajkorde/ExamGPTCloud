import json
import os
from typing import Any, Optional

from domain.model.utils.logging import app_logger

logger = app_logger.get_logger()


def get_env_var(name: str) -> Optional[str]:
    value = os.environ[name]
    if not value:
        logger.error("Could not find bucket name in environment variables")
        return None
    return value


def get_error(message: str = "Something went wrong!") -> dict[str, Any]:
    return {
        "statusCode": 400,
        "body": json.dumps(
            {
                "message": message,
            }
        ),
    }
