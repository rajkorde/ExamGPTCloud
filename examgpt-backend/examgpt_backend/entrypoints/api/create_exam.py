import json
import os
from dataclasses import asdict
from typing import Any

import boto3

# from botocore.exceptions import ClientError
from domain.command_handlers.content_commands_handler import create_upload_urls
from domain.commands.content_commands import CreateUploadURLs
from domain.model.core.exam import Exam
from domain.model.utils.logging import app_logger
from domain.model.utils.misc import ErrorMessage, get_env_var

# from domain.ports.content_service import ContentService
from entrypoints.helpers.utils import get_content_service, get_error
from entrypoints.models.api_model import CreateExamRequest

# from pydantic import ValidationError

ddb = boto3.resource("dynamodb")

logger = app_logger.get_logger()


# def save_exam(exam: Exam, table_name: str):
#     table = ddb.Table(table_name)
#     try:
#         table.put_item(Item=exam.model_dump())
#     except ValidationError as e:
#         print(f"Validation error: {e}")


def handler(event: dict[Any, Any], context: Any) -> dict[str, Any]:
    if not (exam_table := get_env_var("EXAM_TABLE")):
        return get_error("Environment Variable EXAM_TABLE not set correctly.")

    logger.info(f"Exam Table: {exam_table}")

    exam_request = CreateExamRequest.parse_event(event)
    if not exam_request:
        return get_error("Malformed request.")

    logger.info(f"{exam_request=}")

    exam = (
        Exam(
            name=exam_request.exam_name,
            exam_code=exam_request.exam_code,
        )
        if exam_request.exam_code
        else Exam(
            name=exam_request.exam_name,
        )
    )

    logger.info("exam = " + str(exam))

    for filename in exam_request.filenames:
        filename = f"{exam.exam_code}/sources/{os.path.basename(filename)}"
        exam.sources.append(filename)
        logger.info(f"Updated filename: {filename}")

    content_service = get_content_service()
    if not content_service:
        return get_error(
            "Could not retrieve the correct content service. Is the environment variable LOCATION set correctly?"
        )
    signed_urls = create_upload_urls(
        CreateUploadURLs(sources=exam.sources), content_service
    )

    logger.info(f"{signed_urls=}")

    if isinstance(signed_urls, ErrorMessage):
        return get_error("Could not get upload urls")

    # save_exam(exam, exam_table)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "urls": [asdict(signed_url) for signed_url in signed_urls],
                "exam_code": exam.exam_code,
            }
        ),
    }
