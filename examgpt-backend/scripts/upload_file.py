from typing import Any

import boto3
import requests

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
        print(f"Warning:{apis["items"]} API endpoints found. Using the first one.")
    api = apis["items"][0]

    return f"https://{api['id']}.execute-api.{region}.amazonaws.com/{stage}/create_exam"


def upload_file_to_s3(presigned_url: str, fields: dict[str, Any], file_path: str):
    # TODO: perform file size checks
    with open(file_path, "rb") as file:
        files = {"file": (file_path, file)}
        response = requests.post(presigned_url, data=fields, files=files)

    response.raise_for_status()


def main() -> None:
    api_url = get_api_url()
    print(f"Using api: {api_url}")

    print("Requesting presigned URL...")
    response = requests.post(api_url, json=payload)
    response.raise_for_status()

    url = response.json()["urls"][0]["api_url"]
    fields = response.json()["urls"][0]["fields"]
    print(f"Got presigned URL: {url}")

    print("Uploading file...")
    upload_file_to_s3(url, fields, file_path=payload["filenames"][0])
    print("File uploaded successfully")


if __name__ == "__main__":
    main()
