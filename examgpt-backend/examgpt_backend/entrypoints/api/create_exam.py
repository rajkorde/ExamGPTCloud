import json
from dataclasses import asdict
from typing import Any

from domain.command_handlers.content_commands_handler import create_upload_urls
from domain.command_handlers.exam_commands_handler import save_exam
from domain.commands.content_commands import CreateUploadURLs
from domain.commands.exam_commands import SaveExam
from domain.model.utils.logging import app_logger
from domain.ports.data_service import DataService
from entrypoints.helpers.utils import CommandRegistry, get_error
from entrypoints.models.api_model import CreateExamRequest

logger = app_logger.get_logger()


def handler(event: dict[Any, Any], context: Any) -> dict[str, Any]:
    command_registry = CommandRegistry()
    content_service = command_registry.get_content_service()
    exam_service = command_registry.get_exam_service()

    logger.info(event)

    exam_request = CreateExamRequest.parse_event(event)
    if not exam_request:
        return get_error("Malformed request.", error_code=400)

    exam = DataService.create_exam(
        name=exam_request.exam_name,
        filenames=exam_request.filenames,
        exam_code=exam_request.exam_code,
    )

    logger.debug("exam = " + str(exam))

    signed_urls = create_upload_urls(
        CreateUploadURLs(sources=exam.sources), content_service
    )

    logger.debug(f"{signed_urls=}")

    logger.info("Saving Exam to DB")
    response = save_exam(SaveExam(exam=exam), exam_service)
    if not response:
        return get_error(f"Could not save Exam: {exam.exam_code}")

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
        },
        "body": json.dumps(
            {
                "urls": [asdict(signed_url) for signed_url in signed_urls],
                "exam_code": exam.exam_code,
            }
        ),
    }
