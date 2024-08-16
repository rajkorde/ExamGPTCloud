import json
import os
from typing import Any

import boto3
from domain.chunker.pdf_chunker import SimplePDFChunker
from domain.command_handlers.content_commands_handler import download_file
from domain.commands.content_commands import DownloadFile
from domain.model.core.chunk import TextChunk
from domain.model.utils.logging import app_logger
from entrypoints.helpers.utils import CommandRegistry, get_error
from entrypoints.models.api_model import ChunkerRequest
from langchain_community.document_loaders import PyMuPDFLoader
from pydantic import ValidationError

logger = app_logger.get_logger()

s3 = boto3.client("s3")
sns = boto3.client("sns")
ddb = boto3.resource("dynamodb")
CHUNK_BATCH_SIZE = 10


def read_pdf_from_s3(bucket_name: str, object_key: str):
    local_filename = "/tmp/temp.pdf"
    # TODO: add try/catch
    s3.download_file(bucket_name, object_key, local_filename)
    print(f"Filesize: {os.path.getsize(local_filename)}")

    # Use PyMuPDFLoader to load the PDF
    loader = PyMuPDFLoader(local_filename)
    pages = loader.load()
    # Print the number of pages
    print(f"The PDF has {len(pages)} pages.")
    return pages


def get_bucket_name(event: dict[str, Any]):
    s3_obj = event["Records"][0]["s3"]
    bucket_name = s3_obj["bucket"]["name"]
    object_key = s3_obj["object"]["key"]
    return bucket_name, object_key


def save_chunk(chunk: TextChunk, table_name: str):
    table = ddb.Table(table_name)
    try:
        table.put_item(Item=chunk.to_dict())
    except ValidationError as e:
        print(f"Validation error: {e}")


def handler(event: dict[str, Any], context: Any):
    print(event)

    message = "In Chunking code"
    command_registry = CommandRegistry()
    content_service = command_registry.get_content_service()
    # exam_service = command_registry.get_exam_service()

    # Download File
    chunker_request = ChunkerRequest.parse_event(event)
    if not chunker_request:
        print("Error: Could not parse event")
        return get_error("Malformed S3 event", error_code=400)
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
    logger.debug(chunks[33].to_dict())

    # ADD a way to clean and combine chunks!

    # Save chunks in batch
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
