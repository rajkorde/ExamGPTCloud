import os
from typing import Any

import boto3
from domain.command_handlers.chunks_commands_handler import get_chunks
from domain.commands.chunks_commands import GetChunks
from domain.model.utils.logging import app_logger
from entrypoints.helpers.utils import CommandRegistry, get_error, get_success
from entrypoints.models.api_model import GenerateQARequest

# from ai.model_providers
# logger = app_logger.get_logger()
ssm = boto3.client("ssm")
openai_key_name = "/examgpt/OPENAI_API_KEY"

ddb = boto3.resource("dynamodb")
logger = app_logger.get_logger()


def get_parameter(parameter_name: str, with_decryption: bool = True):
    try:
        response = ssm.get_parameter(
            Name=parameter_name, WithDecryption=with_decryption
        )
        return str(response["Parameter"]["Value"])
    except ssm.exceptions.ParameterNotFound:
        logger.error(f"The parameter {parameter_name} was not found.")
        return None
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return None


def handler(event: dict[str, Any], context: Any):
    logger.debug(f"{event=}")
    message = "Generating QAs based on notifcation."
    logger.debug(message)

    command_registry = CommandRegistry()
    chunk_service = command_registry.get_chunk_service()

    # parse request (Get all chunks)
    qa_request = GenerateQARequest.parse_event(event)
    if not qa_request:
        logger.error("Error: Could not parse event")
        return get_error()

    chunk_ids = qa_request.chunk_ids
    if not len(chunk_ids):
        logger.debug("No chunks ids found in message.")
        return get_success("Nothing to process.")

    # get all chunks, ensure all chunks exist and the state is not processed
    chunks = get_chunks(GetChunks(chunk_ids=chunk_ids), chunk_service=chunk_service)
    if not chunks:
        logger.error("Error: Could not get chunks")
        return get_error()
    logger.debug(f"{chunks=}")

    # Create QA objects for each chunk, if not already created
    ## Get OpenAI key
    ## Create OpenAI model
    ## Create QA objects

    # Update Chunk states

    # Save QA objects to DynamoDB

    # Update Chunk states

    # Update Exam state

    # Notify validator lambda

    # return 200

    chunk_table = os.environ["CHUNK_TABLE"]
    if not chunk_table:
        logger.error("Error: Could not find chunk table in environment variables")
    logger.debug(f"{chunk_table=}")

    key = get_parameter(parameter_name=openai_key_name)
    keyname = openai_key_name.split("/")[-1]
    if not key:
        logger.error(f"Error: Incorrect key from ssm parameter store: {key}")
    else:
        os.environ[keyname] = key
    logger.debug(f"{key=}")

    chunk = event["Records"][0]["Sns"]["Message"]
    logger.debug(f"{chunk=}")

    # model = OpenAIProvider()
    # chat = model.get_chat_model()

    # messages = [
    #     (
    #         "system",
    #         "You are a helpful assistant that summarizes paragraphs",
    #     ),
    #     ("human", chunk),
    # ]

    # response = chat.invoke(messages)
    # print(response.content)

    return get_success()
