import random
from typing import Any, Optional

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import BotoCoreError, ClientError
from domain.model.core.chunk import TextChunk, TextChunkState
from domain.model.core.exam import Exam, ExamState
from domain.model.core.question import FlashCardEnhanced, MultipleChoiceEnhanced
from domain.model.utils.exceptions import (
    ExamAlreadyExists,
    InvalidEnvironmentSetup,
    InvalidExam,
    NotEnoughQuestionsInExam,
)
from domain.model.utils.logging import app_logger
from domain.model.utils.misc import get_env_var
from domain.ports.data_service import ChunkService, ExamService, QAService
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

    def _check_exam_exists(self, key: dict[str, str]) -> bool:
        try:
            response = self.table.get_item(Key=key)
            return "Item" in response
        except ClientError as e:
            logger.error(f"Error checking item existence: {e}")
            return False

    def put_exam(self, exam: Exam, overwrite: bool = False) -> bool:
        item = exam.model_dump()
        item["state"] = ExamState.SAVED.value

        if not exam or not exam.exam_code:
            raise InvalidExam()

        if not overwrite:
            if self._check_exam_exists({"exam_code": exam.exam_code}):
                raise ExamAlreadyExists(var=exam.exam_code)

        try:
            self.table.put_item(
                Item=item,
                # ConditionExpression="attribute_not_exists(exam_code)",
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
        response = self.put_exam(exam, overwrite=True)
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

    def get_chunks(self, chunk_ids: list[str]) -> Optional[list[TextChunk]]:
        try:
            logger.info(f"Retrieving chunk items with keys {chunk_ids}")
            batch_keys = {
                self.table.name: {
                    "Keys": [{"chunk_id": chunk_id} for chunk_id in chunk_ids]
                }
            }
            logger.info(batch_keys)

            response = self.ddb.batch_get_item(
                RequestItems={
                    self.table.name: {
                        "Keys": [{"chunk_id": chunk_id} for chunk_id in chunk_ids]
                    }
                }
            )

            if response.get("UnprocessedKeys"):
                logger.error(f"Unprocessed keys: {response.get('UnprocessedKeys')}")
                return None
            items = response["Responses"][self.table.name]
            items = [
                (lambda item: item.update({"state": TextChunkState(item["state"])}))(
                    item
                )
                for item in items
            ]
            return [TextChunk(**item) for item in items]
        except (ClientError, BotoCoreError) as e:
            logger.error(f"Error retrieving chunk items with keys {chunk_ids}: {e}")
            return None


class QAServiceDynamodb(QAService):
    def __init__(self):
        QA_TABLE_ENV_VAR: str = "QA_TABLE"
        table_name = get_env_var(QA_TABLE_ENV_VAR)
        if not table_name:
            raise InvalidEnvironmentSetup(QA_TABLE_ENV_VAR)
        self.ddb = boto3.resource("dynamodb")
        self.table = self.ddb.Table(table_name)

    def save_flashcards(self, flashcards: list[FlashCardEnhanced]) -> bool:
        try:
            with self.table.batch_writer() as batch:
                for flashcard in flashcards:
                    item = flashcard.dict()
                    batch.put_item(Item=item)
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return False
        return True

    def save_multiplechoices(
        self, multiplechoices: list[MultipleChoiceEnhanced]
    ) -> bool:
        try:
            with self.table.batch_writer() as batch:
                for multiplechoice in multiplechoices:
                    item = multiplechoice.dict()
                    batch.put_item(Item=item)
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return False
        return True

    def get_items_by_exam_code(self, exam_code: str) -> Optional[list[dict[str, Any]]]:
        try:
            response = self.table.query(
                KeyConditionExpression=Key("exam_code").eq(exam_code),
            )
        except (ClientError, BotoCoreError) as e:
            logger.error(f"Error retrieving items with exam code {exam_code}: {e}")
            return None

        return response.get("Items", [])

    def get_flashcards(
        self, exam_code: str, n: int = 0
    ) -> Optional[list[FlashCardEnhanced]]:
        items = self.get_items_by_exam_code(exam_code)

        if not items:
            return None

        flashcards = [
            FlashCardEnhanced(**item) for item in items if item["type"] == "flashcard"
        ]

        if n > len(flashcards):
            logger.warning(f"Requested {n} flashcards but only {len(flashcards)} found")
            raise NotEnoughQuestionsInExam(exam_code=exam_code)

        return random.sample(flashcards, n) if n > 0 else flashcards

    def get_multiplechoices(
        self, exam_code: str, n: int = 0
    ) -> Optional[list[MultipleChoiceEnhanced]]:
        items = self.get_items_by_exam_code(exam_code)

        if not items:
            return None

        multiplechoices = [
            MultipleChoiceEnhanced(**item)
            for item in items
            if item["type"] == "multiplechoice"
        ]

        if n > len(multiplechoices):
            logger.warning(
                f"Requested {n} multiple choice questions but only {len(multiplechoices)} found"
            )
            raise NotEnoughQuestionsInExam(exam_code=exam_code)

        return random.sample(multiplechoices, n) if n > 0 else multiplechoices
