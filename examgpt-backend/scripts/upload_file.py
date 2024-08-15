from pathlib import Path
from typing import Any

import boto3
import requests
from loguru import logger

region = "us-west-2"
stage = "Stage"

payload = {
    "exam_name": "AWS Solution Architect Associate Certification Exam",
    "filenames": ["scripts/testdata/aws2.pdf"],
}


def get_api_url():
    client = boto3.client("apigateway", region_name=region)
    apis = client.get_rest_apis()
    if len(apis["items"]) > 1:
        logger.warning(f"{apis["items"]} API endpoints found. Using the first one.")
    api = apis["items"][0]

    return f"https://{api['id']}.execute-api.{region}.amazonaws.com/{stage}/create_exam"


def get_presigned_url(api_url: str, file_path: str):
    exam = {"exam_name": exam_name, "filename": file_path}
    response = requests.post(api_url, json=exam)
    response.raise_for_status()
    presigned_url = response.json()["url"]["url"]
    fields = response.json()["url"]["fields"]
    exam_id = response.json()["exam_id"]
    return presigned_url, fields, exam_id


def upload_file_to_s3(
    presigned_url: str, fields: dict[str, Any], file_path: str
) -> None:
    # TODO: perform file size checks
    with open(file_path, "rb") as file:
        files = {"file": (file_path, file)}
        response = requests.post(presigned_url, data=fields, files=files)

    response.raise_for_status()


def main() -> None:
    api_url = get_api_url()
    print(f"Using api: {api_url}")
    url, fields, exam_id = get_presigned_url(api_url, file_path)
    print("Presigned S3 url generated.")
    print(url)
    print(f"Exam code: {exam_id}")

    if not Path(file_path).exists():
        print(f"Error: file not found: {file_path}")
        return
    upload_file_to_s3(url, fields, file_path=file_path)
    print("File uploaded successfully")


if __name__ == "__main__":
    main()
