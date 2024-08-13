from typing import Any

import boto3
from domain.model.core.exam import Exam
from domain.model.utils.logging import app_logger
from domain.model.utils.misc import ErrorMessage, get_env_var
from pydantic import ValidationError

logger = app_logger.get_logger()
ddb = boto3.resource("dynamodb")
EXAM_TABLE_ENV_VAR: str = "EXAM_TABLE"


class ExamServiceDynamoDB:
    def __init__(self):
        self.table_name = get_env_var(EXAM_TABLE_ENV_VAR)
        if not self.table_name:
            raise RuntimeError(
                f"Environment Variable {EXAM_TABLE_ENV_VAR} not set correctly."
            )

    def put_exam(self, exam: Exam) -> Any:
        table = ddb.Table(self.table_name)
        try:
            table.put_item(Item=exam.model_dump())
        except ValidationError as e:
            print(f"Validation error: {e}")

    def get_exam(self, exam_code: str) -> Any: ...
