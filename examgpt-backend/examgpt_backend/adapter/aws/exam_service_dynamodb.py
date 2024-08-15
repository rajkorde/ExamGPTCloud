from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from domain.model.core.exam import Exam, ExamState
from domain.model.utils.exceptions import InvalidEnvironmentSetup
from domain.model.utils.logging import app_logger
from domain.model.utils.misc import get_env_var
from domain.ports.exam_service import ExamService

logger = app_logger.get_logger()
EXAM_TABLE_ENV_VAR: str = "EXAM_TABLE"


class ExamServiceDynamoDB(ExamService):
    def __init__(self):
        table_name = get_env_var(EXAM_TABLE_ENV_VAR)
        if not table_name:
            raise InvalidEnvironmentSetup(EXAM_TABLE_ENV_VAR)
        self.ddb = boto3.resource("dynamodb")
        self.table = self.ddb.Table(table_name)

    def put_exam(self, exam: Exam) -> bool:
        item = exam.model_dump()
        item["state"] = ExamState.SAVED.value

        try:
            self.table.put_item(
                Item=item,
                ConditionExpression="attribute_not_exists(exam_code)",
            )
            logger.info(f"Exam saved successfully: {exam.exam_code}")
            return True
        except (ClientError, BotoCoreError) as e:
            logger.error(f"Failed saving to Exam table: {e}")
            return False

    def get_exam(self, exam_code: str) -> Optional[Exam]:
        try:
            response = self.table.get_item(Key={"exam_code": exam_code})
            item = response.get("Item")
            item["state"] = ExamState(item["state"])
            if item:
                return Exam(**item)
            return None
        except (ClientError, BotoCoreError) as e:
            logger.error(f"Error retrieving exam item with key {exam_code}: {e}")
            return None
