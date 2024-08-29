from typing import Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from domain.model.core.chunk import TextChunk
from domain.model.core.exam import Exam, ExamState
from domain.model.utils.exceptions import InvalidEnvironmentSetup
from domain.model.utils.logging import app_logger
from domain.model.utils.misc import get_env_var
from domain.ports.data_service import ChunkService, ExamService
from pydantic import ValidationError

logger = app_logger.get_logger()


class ExamServiceDynamoDB(ExamService):
    def __init__(self):
        EXAM_TABLE_ENV_VAR: str = "EXAM_TABLE"
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

    def update_state(self, exam_code: str, newstate: ExamState) -> bool:
        exam = self.get_exam(exam_code)
        if not exam:
            logger.error(f"Exam with this code not while updating state: f{exam_code}")
            return False

        exam.state = newstate
        response = self.put_exam(exam)
        if not response:
            logger.error(f"Failed to update state for exam: {exam_code}")
            return False
        return True


class ChunkServiceDynamoDB(ChunkService):
    def __init__(self):
        CHUNKS_TABLE_ENV_VAR: str = "CHUNK_TABLE"
        table_name = get_env_var(CHUNKS_TABLE_ENV_VAR)
        if not table_name:
            raise InvalidEnvironmentSetup(CHUNKS_TABLE_ENV_VAR)
        self.ddb = boto3.resource("dynamodb")
        self.table = self.ddb.Table(table_name)

    def save_chunks(self, chunks: list[TextChunk]) -> bool:
        try:
            with self.table.batch_writer() as batch:
                for chunk in chunks:
                    item = chunk.model_dump()
                    item["state"] = chunk.state.value
                    batch.put_item(Item=item)
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return False
        return True
