from typing import Optional

from domain.commands.questions_commands import CreateFlashCard, CreateMultipleChoice
from domain.model.core.question import FlashCardEnhanced, MultipleChoiceEnhanced
from domain.ports.ai_service import AIService


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


def create_flash_cards(
    commands: list[CreateFlashCard], ai_service: AIService
) -> Optional[list[FlashCardEnhanced]]:
    flash_cards = []
    for command in commands:
        flash_cards.append(create_flash_card(command, ai_service))

    return flash_cards


def create_multiple_choices(
    commands: list[CreateMultipleChoice], ai_service: AIService
) -> Optional[list[MultipleChoiceEnhanced]]:
    multiple_choices = []
    for command in commands:
        multiple_choices.append(create_multiple_choice(command, ai_service))

    return multiple_choices
