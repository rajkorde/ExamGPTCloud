from domain.ai.base import BaseModelProvider
from domain.model.core.chunk import TextChunk
from domain.model.core.question import FlashCardEnhanced, MultipleChoiceEnhanced
from langchain.pydantic_v1 import BaseModel as BM1
from pydantic import BaseModel as BM2
from pydantic import ConfigDict


class SaveFlashCards(BM1):
    flash_cards: list[FlashCardEnhanced]


class SaveMultipleChoices(BM1):
    multiple_choices: list[MultipleChoiceEnhanced]


class GetFlashCards(BM2):
    exam_code: str
    n: int = 0


class GetMultipleChoices(BM2):
    exam_code: str
    n: int = 0


class CreateFlashCard(BM2):
    model_config = ConfigDict(protected_namespaces=())

    chunk: TextChunk
    exam_code: str
    exam_name: str
    model_provider: BaseModelProvider


class CreateMultipleChoice(BM2):
    model_config = ConfigDict(protected_namespaces=())

    chunk: TextChunk
    exam_code: str
    exam_name: str
    model_provider: BaseModelProvider
