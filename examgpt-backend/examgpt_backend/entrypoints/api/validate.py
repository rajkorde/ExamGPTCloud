from typing import Any

from domain.command_handlers.exam_commands_handler import get_exam
from domain.commands.exam_commands import GetExam
from domain.model.utils.logging import app_logger
from entrypoints.helpers.utils import CommandRegistry, get_error, get_success
from entrypoints.models.api_model import ValidateRequest

logger = app_logger.get_logger()


def handler(event: dict[Any, Any], context: Any) -> dict[str, Any]:
    logger.info("Executing validator.")
    logger.info(f"{event=}")

    command_registry = CommandRegistry()
    exam_service = command_registry.get_exam_service()

    exam_event = ValidateRequest.parse_event(event)
    if not exam_event:
        logger.error("Error: Could not parse event")
        return get_error()

    exam_code = exam_event.exam_code

    # Get exam and validate state is at least chunked and not ready
    exam = get_exam(GetExam(exam_code=exam_code), exam_service)

    # Get chunks

    # Validate state of chunks

    # Get QA

    # print stats of chunks and QA

    # Set exam state to Ready

    # notify user that exam is ready

    return get_success()
