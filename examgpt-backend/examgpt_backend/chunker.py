import json
import os
from typing import Any

import boto3
from langchain_community.document_loaders import PyMuPDFLoader

s3 = boto3.client("s3")
sns = boto3.client("sns")


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


def handler(event: dict[str, Any], context: Any):
    message = "In Chunking code"
    print(f"{event=}")
    print(f"{message=}")

    bucket_name, object_key = get_bucket_name(event)
    print(f"{bucket_name}=")
    print(f"{object_key}=")
    pages = read_pdf_from_s3(bucket_name, object_key)
    chunk = pages[65].page_content
    print(chunk)

    topic_name = os.environ["CHUNKS_TOPIC"]
    print(topic_name)

    sns.publish(
        TopicArn=topic_name,
        Message=json.dumps({"default": chunk}),
        MessageStructure="json",
    )

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": message,
            }
        ),
    }
