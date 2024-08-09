import sys
from typing import Any

from loguru import logger


class ApplicationLogger:
    log_level: str = "DEBUG"

    def __init__(self, **kwargs: Any):
        self.configure_logging(self.log_level)

    def configure_logging(self, level: str):
        logger.remove()
        logger.add(
            sys.stderr,
            format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        )

    def get_logger(self):
        return logger


app_logger = ApplicationLogger()
