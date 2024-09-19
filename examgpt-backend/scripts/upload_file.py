import os
from typing import Any

import requests
from lib.utils import get_api_url, get_env, load_env_files


def upload_file_to_s3(presigned_url: str, fields: dict[str, Any], file_path: str):
    # TODO: perform file size checks
    with open(file_path, "rb") as file:
        files = {"file": (file_path, file)}
        response = requests.post(presigned_url, data=fields, files=files)

    response.raise_for_status()


def main() -> None:
    load_env_files()
    stage = get_env("STAGE")
    region = get_env("REGION")

    payload = {
        "exam_name": "AWS Solution Architect Associate Certification Exam",
        "email": os.getenv("EMAIL"),
        "filenames": ["scripts/testdata/aws2.pdf"],
    }

    api_url = get_api_url("create_exam", stage, region)
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
