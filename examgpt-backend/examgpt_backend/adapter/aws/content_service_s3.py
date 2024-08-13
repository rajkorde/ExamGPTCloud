from dataclasses import dataclass
from typing import Any

import boto3
from botocore.exceptions import ClientError
from domain.model.utils.logging import app_logger
from domain.model.utils.misc import ErrorMessage, get_env_var
from domain.ports.content_service import ContentService

s3 = boto3.client("s3")
CONTENT_ENV_VAR: str = "CONTENT_BUCKET"
logger = app_logger.get_logger()


@dataclass
class PreSignedUrl:
    api_url: str
    fields: dict[str, Any]


class ContentServiceS3(ContentService):
    def create_upload_url(
        self, filename: str, expires_in: int = 3600
    ) -> PreSignedUrl | ErrorMessage:
        if not (bucket_name := get_env_var(CONTENT_ENV_VAR)):
            return ErrorMessage(
                f"Environment Variable {CONTENT_ENV_VAR} not set correctly."
            )
        try:
            response = s3.generate_presigned_post(
                bucket_name,
                filename,
                Fields=None,
                Conditions=None,
                ExpiresIn=expires_in,
            )
        except ClientError as e:
            logger.error(e)
            return ErrorMessage("Could not generate presigned S3 URL")

        # The response contains the presigned URL
        api_url = response["url"]
        fields = response["fields"]
        return PreSignedUrl(api_url, fields)
