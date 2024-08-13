import datetime
import os
from dataclasses import dataclass, field
from typing import Optional

from domain.model.utils.logging import app_logger

logger = app_logger.get_logger()


@dataclass
class ErrorMessage:
    message: str = field(default="Something went wrong")


def get_env_var(name: str) -> Optional[str]:
    value = os.environ[name]
    if not value:
        logger.error(f"Could not find environment variable: {name}")
        return None
    return value


def get_current_time() -> str:
    """Gets the current date and time as a string."""
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    return str(timestamp)
