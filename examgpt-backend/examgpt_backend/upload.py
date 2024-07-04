import json
import logging
import os

import boto3

s3 = boto3.client("s3")
logger = logging.getLogger(__name__)


def create_presigned_url(bucket_name, object_name, expiration=3600):
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


def handler(event, context):
    message = "In uploading code"
    print(f"{event=}")
    print(f"{message=}")

    bucket_name = os.environ["CONTENT_BUCKET"]
    print(f"{bucket_name=}")
    signed_url = create_presigned_url(bucket_name, object_name="test")
    if not signed_url:
        message = "Something went wrong in creating presigned URL"

    print(f"{signed_url=}")
    message = f"{message}: {signed_url}"

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": message,
            }
        ),
    }
