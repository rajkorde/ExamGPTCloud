import json
import logging
import os
from typing import Any, Optional

import boto3
from botocore.exceptions import ClientError

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


def handler(event: dict[Any, Any], context: Any) -> dict[str, Any]:
    bucket_name = os.environ["CONTENT_BUCKET"]
    if not bucket_name:
        logger.error("Could not find bucket name in environment variables")
        return get_error()

    body_json = json.loads(event["body"])
    if "filename" in body_json:
        filename = body_json["filename"]
    else:
        print("No property called filename in request")
        print(f"{event=}")
        filename = "test/test.pdf"
    print(f"Received request for uploading file: {filename}")

    signed_url = create_presigned_url(bucket_name, object_name=filename)
    if not signed_url:
        message = "Could not generate pre-signed URL"
        logger.error(message)
        return get_error(message)

    print("Generated presigned URL.")

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "url": signed_url,
            }
        ),
    }
