from typing import Optional

from domain.commands.questions_commands import (
    CreateFlashCard,
    CreateMultipleChoice,
    GetFlashCards,
    GetMultipleChoices,
    SaveFlashCards,
    SaveMultipleChoices,
)
from domain.model.core.question import FlashCardEnhanced, MultipleChoiceEnhanced
from domain.ports.ai_service import AIService
from domain.ports.data_service import QAService


def create_flash_card(
    command: CreateFlashCard,
    ai_service: AIService,
) -> Optional[list[FlashCardEnhanced]]:
    return ai_service.create_flash_card(
        command.chunk, command.exam_code, command.exam_name, command.model_provider
    )


def create_multiple_choice(
    command: CreateMultipleChoice, ai_service: AIService
) -> Optional[list[MultipleChoiceEnhanced]]:
    return ai_service.create_multiple_choice(
        command.chunk, command.exam_code, command.exam_name, command.model_provider
    )


def save_flashcards(command: SaveFlashCards, data_service: QAService) -> bool:
    return data_service.save_flashcards(command.flash_cards)


def save_multiplechoices(command: SaveMultipleChoices, data_service: QAService) -> bool:
    return data_service.save_multiplechoices(command.multiple_choices)


def get_flashcards(
    command: GetFlashCards, data_service: QAService
) -> Optional[list[FlashCardEnhanced]]:
    return data_service.get_flashcards(command.exam_code, command.n)


def get_multiplechoices(
    command: GetMultipleChoices, data_service: QAService
) -> Optional[list[MultipleChoiceEnhanced]]:
    return data_service.get_multiplechoices(command.exam_code, command.n)
