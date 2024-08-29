import json
from typing import Any

import boto3
from domain.chunker.pdf_chunker import SimplePDFChunker
from domain.command_handlers.chunks_commands_handler import save_chunks
from domain.command_handlers.content_commands_handler import download_file
from domain.commands.chunks_commands import SaveChunks
from domain.commands.content_commands import DownloadFile
from domain.model.utils.logging import app_logger
from entrypoints.helpers.utils import CommandRegistry, get_error
from entrypoints.models.api_model import ChunkerRequest

logger = app_logger.get_logger()

s3 = boto3.client("s3")
sns = boto3.client("sns")
ddb = boto3.resource("dynamodb")
CHUNK_BATCH_SIZE = 10


# def save_chunk(chunk: TextChunk, table_name: str):
#     table = ddb.Table(table_name)
#     try:
#         table.put_item(Item=chunk.model_dump())
#     except ValidationError as e:
#         print(f"Validation error: {e}")


def handler(event: dict[str, Any], context: Any):
    print(event)

    message = "In Chunking code"
    command_registry = CommandRegistry()
    content_service = command_registry.get_content_service()
    # exam_service = command_registry.get_exam_service()

    # Download File
    chunker_request = ChunkerRequest.parse_event(event)
    if not chunker_request:
        logger.error("Error: Could not parse event")
        return get_error()
    exam_code = chunker_request.exam_code

    downloaded_file = download_file(
        command=DownloadFile(
            source=chunker_request.location, bucket_name=chunker_request.bucket_name
        ),
        content_service=content_service,
    )
    logger.debug(f"{downloaded_file=}")

    # Chunk file
    chunker = SimplePDFChunker()
    chunks = chunker.chunk(location=downloaded_file, exam_code=exam_code)
    logger.debug(f"Chunks size: {len(chunks)}")
    logger.debug(chunks[33].model_dump())

    # Save chunks in batch
    chunk_service = command_registry.get_chunk_service()
    response = save_chunks(SaveChunks(chunks=chunks), chunk_service)
    if not response:
        logger.error("Error: Could not save chunks")
        return get_error()

    # Publish chunk topic in batches
    # Update Exam state

    # chunk_table = os.environ["CHUNK_TABLE"]
    # if not chunk_table:
    #     print("Error: Could not find chunk table in environment variables")

    # message = "In Chunking code"
    # print(f"{event=}")
    # print(f"{message=}")

    # bucket_name, object_key = get_bucket_name(event)
    # print(f"{bucket_name}=")
    # print(f"{object_key}=")

    # folders = object_key.split("/")
    # if len(folders) != 3:
    #     print(
    #         f"Error: the object key does not have the right folder structure: {object_key}"
    #     )
    # exam_id = folders[0]

    # pages = read_pdf_from_s3(bucket_name, object_key)

    # chunk_ids = []
    # for i, page in enumerate(pages):
    #     chunk = TextChunk(exam_id=exam_id, text=page.page_content, page_number=i)
    #     chunk_ids.append(chunk.chunk_id)
    #     save_chunk(chunk, chunk_table)

    # topic_name = os.environ["CHUNK_TOPIC"]
    # print(topic_name)

    # sns.publish(
    #     TopicArn=topic_name,
    #     Message=json.dumps({"default": str(chunk_ids[:CHUNK_BATCH_SIZE])}),
    #     MessageStructure="json",
    # )

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": message,
            }
        ),
    }
