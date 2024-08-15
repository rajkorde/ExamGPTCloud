import os
from dataclasses import dataclass
from typing import Any

import boto3
from botocore.exceptions import ClientError
from domain.model.utils.exceptions import InvalidEnvironmentSetup
from domain.model.utils.logging import app_logger
from domain.model.utils.misc import get_env_var
from domain.ports.content_service import ContentService

s3 = boto3.client("s3")
CONTENT_BUCKET_ENV_VAR: str = "CONTENT_BUCKET"
logger = app_logger.get_logger()


@dataclass
class PreSignedUrl:
    api_url: str
    fields: dict[str, Any]


class ContentServiceS3(ContentService):
    def __init__(self):
        self.bucket_name = get_env_var(CONTENT_BUCKET_ENV_VAR)
        if not self.bucket_name:
            raise InvalidEnvironmentSetup(CONTENT_BUCKET_ENV_VAR)
        self.s3 = boto3.client("s3")

    def create_upload_url(self, filename: str, expires_in: int = 3600) -> PreSignedUrl:
        try:
            response = s3.generate_presigned_post(
                self.bucket_name,
                filename,
                Fields=None,
                Conditions=None,
                ExpiresIn=expires_in,
            )
        except ClientError as e:
            logger.error(e)
            raise e

        api_url = response["url"]
        fields = response["fields"]
        return PreSignedUrl(api_url, fields)

    def download_file(self, source: str, destination: str) -> str:
        try:
            self.s3.download_file(self.bucket_name, source, destination)
            logger.debug(f"Filesize: {os.path.getsize(destination)}")
        except ClientError as e:
            logger.error(e)
            raise e
        return destination
