import os
from typing import Any

from domain.command_handlers.chunks_commands_handler import get_chunks, save_chunks
from domain.command_handlers.environments_commands_handler import get_parameter
from domain.command_handlers.exam_commands_handler import get_exam, notify_validate_exam
from domain.command_handlers.questions_commands_handler import (
    create_flash_cards,
    create_multiple_choices,
    save_flashcards,
    save_multiplechoices,
)
from domain.commands.chunks_commands import GetChunks, SaveChunks
from domain.commands.environment_commands import GetParameter
from domain.commands.exam_commands import GetExam, NotifyValidateExam
from domain.commands.questions_commands import (
    CreateFlashCard,
    CreateMultipleChoice,
    SaveFlashCards,
    SaveMultipleChoices,
)
from domain.model.utils.logging import app_logger
from entrypoints.helpers.utils import CommandRegistry, get_error, get_success
from entrypoints.models.api_model import GenerateQARequest

openai_key_name = "/examgpt/OPENAI_API_KEY"
logger = app_logger.get_logger()


def handler(event: dict[str, Any], context: Any):
    logger.debug(f"{event=}")
    logger.debug("Generating QAs based on notifcation.")

    command_registry = CommandRegistry()
    chunk_service = command_registry.get_chunk_service()
    environment_service = command_registry.get_environment_service()
    exam_service = command_registry.get_exam_service()
    qa_service = command_registry.get_qa_service()
    notification_service = command_registry.get_validation_notification_service()

    # parse request (Get all chunks)
    logger.info("Parsing request.")
    qa_request = GenerateQARequest.parse_event(event)
    if not qa_request:
        logger.error("Error: Could not parse event")
        return get_error()

    chunk_ids = qa_request.chunk_ids
    exam_code = qa_request.exam_code
    if not len(chunk_ids):
        logger.debug("No chunks ids found in message.")
        return get_success("Nothing to process.")

    # get all chunks, ensure all chunks exist and the state is not processed
    logger.info("Getting all chunks in the notification from the database.")
    chunks = get_chunks(
        GetChunks(chunk_ids=chunk_ids, exam_code=exam_code), chunk_service=chunk_service
    )
    if not chunks:
        logger.error("Error: Could not get chunks")
        return get_error()
    logger.debug(f"{len(chunks)=}")
    # Ensure exam codes in all text chunks are the same
    assert all(
        chunk.exam_code == exam_code for chunk in chunks
    ), "Not all values in the list are the same"

    # get exam
    logger.info("Getting exam from the database.")
    exam = get_exam(GetExam(exam_code=exam_code), exam_service=exam_service)
    if not exam:
        logger.error("Error: Could not get exam")
        return get_error()
    logger.debug(f"{exam=}")
    exam_name = exam.name

    # Create QA objects for each chunk, if not already created
    ## Get OpenAI key
    logger.info("Getting model key.")
    openai_key = get_parameter(
        GetParameter(name=openai_key_name, is_encrypted=True), environment_service
    )
    if not openai_key:
        logger.error("Error: Could not get OpenAI key")
        return get_error()
    logger.debug(f"{openai_key=}")
    os.environ[openai_key_name.split("/")[2]] = openai_key

    ## Create QA objects
    ai_service = command_registry.get_ai_service()
    model_provider = command_registry.get_model_provider()
    logger.info("Generating flash cards.")
    flash_cards = create_flash_cards(
        [
            CreateFlashCard(
                chunk=chunk,
                exam_code=exam_code,
                exam_name=exam_name,
                model_provider=model_provider,
            )
            for chunk in chunks
            if not chunk.flash_card_generated
        ],
        ai_service,
    )

    logger.info("Generating multiple choice questions.")
    multiple_choices = create_multiple_choices(
        [
            CreateMultipleChoice(
                chunk=chunk,
                exam_code=exam_code,
                exam_name=exam_name,
                model_provider=model_provider,
            )
            for chunk in chunks
            if not chunk.multiple_choice_generated
        ],
        ai_service,
    )

    if (
        not flash_cards
        or not len(flash_cards)
        or not multiple_choices
        or not len(multiple_choices)
    ):
        logger.warning("Could not create any QA objects for chunks")
        return get_error()

    assert flash_cards
    assert multiple_choices

    # Save QA objects to DynamoDB
    logger.info("Saving flash cards to Database.")
    flashcard_response = save_flashcards(
        command=SaveFlashCards(flash_cards=flash_cards), data_service=qa_service
    )
    logger.info("Saving multiple choice questions to Database.")
    multiplechoice_response = save_multiplechoices(
        command=SaveMultipleChoices(multiple_choices=multiple_choices),
        data_service=qa_service,
    )
    if not flashcard_response or not multiplechoice_response:
        logger.error("Error: Could not save QA objects")
        return get_error()

    # Update Chunk states
    logger.info("Updating chunks.")
    [setattr(chunk, "flash_card_generated", True) for chunk in chunks]
    [setattr(chunk, "multiple_choice_generated", True) for chunk in chunks]
    response = save_chunks(
        command=SaveChunks(chunks=chunks), chunk_service=chunk_service
    )
    if not response:
        logger.error("Error: Could not save chunks")
        return get_error()

    # Notify validator lambda
    notify_validate_exam(
        command=NotifyValidateExam(exam_code=exam_code),
        notification_service=notification_service,
    )

    # return 200
    return get_success()
