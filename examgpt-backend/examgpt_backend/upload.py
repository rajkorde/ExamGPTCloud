import json
import logging
import os
from typing import Any, Optional

import boto3
from botocore.exceptions import ClientError
from core.exam import Exam

s3 = boto3.client("s3")
logger = logging.getLogger(__name__)


def create_presigned_url(
    bucket_name: str,
    object_name: str,
    fields: Optional[dict[str, Any]] = None,
    conditions: Optional[list[dict[str, Any]]] = None,
    expiration: int = 3600,
) -> str | None:
    try:
        response = s3.generate_presigned_post(
            bucket_name,
            object_name,
            Fields=fields,
            Conditions=conditions,
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logger.error(e)
        return None

    # The response contains the presigned URL
    return response


def get_error(message: str = "Something went wrong!") -> dict[str, Any]:
    return {
        "statusCode": 400,
        "body": json.dumps(
            {
                "message": message,
            }
        ),
    }


def get_item(body: dict[str, Any], item: str):
    if item not in body:
        print(f"No property called {item} in request")
        return None
    return body[item]


def parse_event(event: dict[Any, Any]):
    body_json = json.loads(event["body"])
    filename = get_item(body_json, "filename")
    exam_name = get_item(body_json, "exam_name")
    return filename, exam_name


def handler(event: dict[Any, Any], context: Any) -> dict[str, Any]:
    bucket_name = os.environ["CONTENT_BUCKET"]
    if not bucket_name:
        logger.error("Could not find bucket name in environment variables")
        return get_error()

    exam_table = os.environ["EXAM_TABLE"]
    if not exam_table:
        logger.error("Could not find exam table in environment variables")
        return get_error()

    print(f"Content Bucket: {bucket_name}")
    print(f"Exam Table: {exam_table}")

    filename, exam_name = parse_event(event)
    if not filename or not exam_name:
        return get_error()
    print(f"Received request for uploading file: {filename}")

    exam = Exam(name=exam_name)
    filename = f"{exam.exam_id}/sources/{os.path.basename(filename)}"
    exam.sources.append(filename)
    print(f"Updated filename: {filename}")

    signed_url = create_presigned_url(bucket_name, object_name=filename)
    if not signed_url:
        message = "Could not generate pre-signed URL"
        logger.error(message)
        return get_error(message)

    print("Generated presigned URL.")

    return {
        "statusCode": 200,
        "body": json.dumps({"url": signed_url, "exam_id": exam.exam_id}),
    }
