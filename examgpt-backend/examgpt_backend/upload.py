import json
import logging
import os
from typing import Any

import boto3

s3 = boto3.client("s3")
logger = logging.getLogger(__name__)


def create_presigned_url(
    bucket_name: str, object_name: str, expiration: int = 3600
) -> str | None:
    try:
        response = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except Exception as e:
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


def handler(event: dict[Any, Any], context) -> dict[str, Any]:
    bucket_name = os.environ["CONTENT_BUCKET"]
    if not bucket_name:
        logger.error("Could not find bucket name in environment variables")
        return get_error()

    signed_url = create_presigned_url(bucket_name, object_name="test")
    if not signed_url:
        message = "Could not generate pre-signed URL"
        logger.error(message)
        return get_error(message)

    print(f"Generated presigned URL: {signed_url}")

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "url": signed_url,
            }
        ),
    }
