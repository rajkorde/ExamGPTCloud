from __future__ import annotations

import json
from typing import Any, Optional

from domain.model.utils.logging import app_logger
from pydantic import BaseModel, Field

logger = app_logger.get_logger()


def handle_error(event: dict[str, Any]):
    logger.error("Invalid event specifiction: {event}")
    return None


class CreateExamRequest(BaseModel):
    exam_name: str = Field(description="Exam Name")
    filenames: list[str] = Field(
        description="List of S3 locations with study material", default_factory=list
    )
    exam_code: Optional[str] = Field(description="Exam code")

    @staticmethod
    def parse_event(
        event: dict[str, Any],
    ) -> CreateExamRequest | None:
        body_str = event.get("body")
        if not body_str:
            return handle_error(event)
        body = json.loads(body_str)

        exam_name = body.get("exam_name")
        if not exam_name:
            return handle_error(event)
        filenames = body.get("filenames")
        if not filenames:
            return handle_error(event)
        exam_code = body.get("exam_code")

        return CreateExamRequest(
            exam_name=exam_name, filenames=filenames, exam_code=exam_code
        )


class ChunkerRequest(BaseModel):
    bucket_name: str = Field(description="Bucket Name")
    location: str = Field(description="Location of the file")
    exam_code: str = Field(description="Exam code")

    @staticmethod
    def _get_bucket_name(event: dict[str, Any]):
        try:
            s3_obj = event["Records"][0]["s3"]
            bucket_name = s3_obj["bucket"]["name"]
            object_key = s3_obj["object"]["key"]
        except Exception as e:
            logger.error(f"Error parsing S3 event: {e}")
            return None
        return bucket_name, object_key

    @staticmethod
    def _get_exam_code(key: str) -> Optional[str]:
        folders = key.split("/")
        if len(folders) != 3:
            print(
                f"Error: the object key does not have the right folder structure: {key}"
            )
            return None
        return folders[0]

    @staticmethod
    def parse_event(
        event: dict[str, Any],
    ) -> ChunkerRequest | None:
        response = ChunkerRequest._get_bucket_name(event)
        if not response:
            return handle_error(event)

        bucket_name, object_key = response
        exam_code = ChunkerRequest._get_exam_code(object_key)
        if not exam_code:
            return handle_error(event)

        logger.debug(f"{bucket_name=}, {object_key=}, {exam_code=}")

        return ChunkerRequest(
            bucket_name=bucket_name, location=object_key, exam_code=exam_code
        )
