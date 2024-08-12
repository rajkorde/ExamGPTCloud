import json
import os
from typing import Any, Optional

import boto3
from botocore.exceptions import ClientError

# from domain.model.core.exam import Exam
from domain.model.utils.logging import app_logger
from entrypoints.helpers.utils import get_env_var, get_error
from entrypoints.models.api_model import CreateExamRequest
from pydantic import ValidationError

s3 = boto3.client("s3")
ddb = boto3.resource("dynamodb")

logger = app_logger.get_logger()


# def save_exam(exam: Exam, table_name: str):
#     table = ddb.Table(table_name)
#     try:
#         table.put_item(Item=exam.model_dump())
#     except ValidationError as e:
#         print(f"Validation error: {e}")


def handler(event: dict[Any, Any], context: Any) -> dict[str, Any]:
    print(event)

    if not (bucket_name := get_env_var("CONTENT_BUCKET")):
        return get_error("Environment Variable CONTENT_BUCKET not set correctly.")

    if not (exam_table := get_env_var("EXAM_TABLE")):
        return get_error("Environment Variable EXAM_TABLE not set correctly.")

    # print(f"Content Bucket: {bucket_name}")
    # print(f"Exam Table: {exam_table}")

    logger.info(f"Content Bucket: {bucket_name}")
    logger.info(f"Exam Table: {exam_table}")

    exam_request = CreateExamRequest.parse_event(event)
    if not exam_request:
        return get_error("Malformed request.")

    logger.info(f"{exam_request=}")

    # filename, exam_name = parse_event(event)
    # if not filename or not exam_name:
    #     return get_error()
    # print(f"Received request for uploading file: {filename}")

    # exam = Exam(name=exam_name)

    # filename = f"{exam.exam_id}/sources/{os.path.basename(filename)}"
    # exam.sources.append(filename)
    # print(f"Updated filename: {filename}")

    # signed_url = create_presigned_url(bucket_name, object_name=filename)
    # if not signed_url:
    #     message = "Could not generate pre-signed URL"
    #     logger.error(message)
    #     return get_error(message)

    # print("Generated presigned URL.")
    # save_exam(exam, exam_table)

    return {
        "statusCode": 200,
        # "body": json.dumps({"url": signed_url, "exam_id": exam.exam_id}),
        "body": "ok",
    }
