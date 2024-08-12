from __future__ import annotations

import json
from typing import Any, Optional

from domain.model.utils.logging import app_logger
from pydantic import BaseModel, Field

logger = app_logger.get_logger()


class CreateExamRequest(BaseModel):
    exam_name: str = Field(description="Exam Name")
    filenames: list[str] = Field(
        description="List of S3 locations with study material", default_factory=list
    )
    exam_code: Optional[str] = Field(description="Exam code")

    @staticmethod
    def _handle_error(event: dict[str, Any]):
        logger.error("Invalid body specifiction in event: {event}")
        return None

    @staticmethod
    def parse_event(
        event: dict[str, Any],
    ) -> CreateExamRequest | None:
        body_str = event.get("body")
        if not body_str:
            return CreateExamRequest._handle_error(event)
        body = json.loads(body_str)

        exam_name = body.get("exam_name")
        if not exam_name:
            return CreateExamRequest._handle_error(event)
        filenames = body.get("filenames")
        if not filenames:
            return CreateExamRequest._handle_error(event)
        exam_code = body.get("exam_code")

        return CreateExamRequest(
            exam_name=exam_name, filenames=filenames, exam_code=exam_code
        )
