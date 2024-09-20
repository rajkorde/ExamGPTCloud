from __future__ import annotations

import json
from typing import Any, Optional

from domain.model.utils.logging import app_logger
from pydantic import BaseModel, EmailStr, Field

logger = app_logger.get_logger()


class CreateExamRequest(BaseModel):
    exam_name: str = Field(description="Exam Name")
    email: EmailStr = Field(description="Email of the exam creator")
    filenames: list[str] = Field(
        description="List of S3 locations with study material", default_factory=list
    )
    exam_code: Optional[str] = Field(description="Exam code")

    @staticmethod
    def parse_event(
        event: dict[str, Any],
    ) -> Optional[CreateExamRequest]:
        body_str = event.get("body")
        if not body_str:
            logger.error(f"Invalid event specifiction: {event}")
            return None
        body = json.loads(body_str)

        exam_name = body.get("exam_name")
        if not exam_name:
            logger.error(f"Invalid exam name specifiction: {event}")
            return None
        filenames = body.get("filenames")
        if not filenames:
            logger.error(f"Invalid filenames specifiction: {event}")
            return None
        email = body.get("email")
        if not email:
            logger.error(f"Invalid email specifiction: {event}")
            return None
        exam_code = body.get("exam_code")

        return CreateExamRequest(
            exam_name=exam_name, email=email, filenames=filenames, exam_code=exam_code
        )


class GenerateQARequest(BaseModel):
    chunk_ids: list[str] = Field(description="List of Chunk IDs")
    exam_code: str = Field(description="Exam code for the chunks")
    last_chunk: bool = Field(description="Is this the last chunk")

    @staticmethod
    def parse_event(event: dict[str, Any]) -> Optional[GenerateQARequest]:
        message = eval(event["Records"][0]["Sns"]["Message"])
        chunk_ids = message["chunk_ids"]
        exam_code = message["exam_code"]
        last_chunk = message["last_chunk"]
        if not chunk_ids or not isinstance(chunk_ids, list) or not exam_code:
            logger.error(f"Invalid event specifiction: {event}")
            return None
        return GenerateQARequest(
            chunk_ids=chunk_ids, exam_code=exam_code, last_chunk=last_chunk
        )


class ValidateRequest(BaseModel):
    exam_code: str = Field(description="Exam code for the exam")

    @staticmethod
    def parse_event(event: dict[str, Any]) -> Optional[ValidateRequest]:
        message = eval(event["Records"][0]["Sns"]["Message"])
        exam_code = message["exam_code"]
        if not exam_code:
            logger.error(f"Invalid event specifiction: {event}")
            return None
        return ValidateRequest(exam_code=exam_code)


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
    ) -> Optional[ChunkerRequest]:
        response = ChunkerRequest._get_bucket_name(event)
        if not response:
            logger.error("Invalid event specifiction: {event}")
            return None

        bucket_name, object_key = response
        exam_code = ChunkerRequest._get_exam_code(object_key)
        if not exam_code:
            logger.error("Invalid event specifiction: {event}")
            return None

        return ChunkerRequest(
            bucket_name=bucket_name, location=object_key, exam_code=exam_code
        )
