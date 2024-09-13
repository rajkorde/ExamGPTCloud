import os
from dataclasses import dataclass
from typing import Any, Optional

import boto3
from botocore.exceptions import ClientError
from domain.model.utils.exceptions import InvalidEnvironmentSetup
from domain.model.utils.logging import app_logger
from domain.model.utils.misc import get_env_var
from domain.ports.content_service import ContentService

s3 = boto3.client("s3")
BUCKET_ENV_VAR: str = "BUCKET_NAME"
logger = app_logger.get_logger()


@dataclass
class PreSignedUrl:
    api_url: str
    fields: dict[str, Any]


class ContentServiceS3(ContentService):
    def __init__(self):
        self.s3 = boto3.client("s3")

    def create_upload_url(self, filename: str, expires_in: int = 3600) -> PreSignedUrl:
        bucket_name = get_env_var(BUCKET_ENV_VAR)
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
            raise e

        api_url = response["url"]
        fields = response["fields"]
        return PreSignedUrl(api_url, fields)

    def download_file(
        self, source: str, destination: str, bucket_name: Optional[str] = None
    ) -> str:
        try:
            if not bucket_name:
                bucket_name = get_env_var(BUCKET_ENV_VAR)
                if not bucket_name:
                    logger.error(
                        "No bucket name provided in function call or in environment variable."
                    )
                    raise InvalidEnvironmentSetup(BUCKET_ENV_VAR)
            self.s3.download_file(bucket_name, source, destination)
            logger.debug(f"Downloaded filesize: {os.path.getsize(destination)}")
        except ClientError as e:
            logger.error(e)
            raise e
        return destination

    def upload_file(
        self, source: str, destination: str, bucket_name: Optional[str] = None
    ) -> str:
        if not os.path.exists(source):
            raise ValueError(f"Souce file does not exist: {source}")
        if not bucket_name:
            bucket_name = get_env_var(BUCKET_ENV_VAR)
            if not bucket_name:
                logger.error(
                    "No bucket name provided in function call or in environment variable."
                )
                raise InvalidEnvironmentSetup(BUCKET_ENV_VAR)
        try:
            self.s3.upload_file(source, bucket_name, destination)
        except ClientError as e:
            logger.error(e)
            raise e
        return destination
