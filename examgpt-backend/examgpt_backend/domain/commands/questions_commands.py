from domain.ai.base import BaseModelProvider
from domain.model.core.chunk import TextChunk
from domain.model.core.question import FlashCardEnhanced, MultipleChoiceEnhanced
from pydantic import BaseModel, ConfigDict


class CreateFlashCard(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    chunk: TextChunk
    exam_code: str
    exam_name: str
    model_provider: BaseModelProvider


class CreateMultipleChoice(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    chunk: TextChunk
    exam_code: str
    exam_name: str
    model_provider: BaseModelProvider


class SaveFlashCards(BaseModel):
    flash_cards: list[FlashCardEnhanced]


class SaveMultipleChoices(BaseModel):
    multiple_choices: list[MultipleChoiceEnhanced]


class GetFlashCards(BaseModel):
    exam_code: str
    n: int = 0


class GetMultipleChoices(BaseModel):
    exam_code: str
    n: int = 0
