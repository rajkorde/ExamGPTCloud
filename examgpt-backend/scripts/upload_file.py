from pathlib import Path
from typing import Any

import requests

api_url = "https://aer2di0h2m.execute-api.us-west-2.amazonaws.com/Stage/upload"
file_path = "testdata/aws2.pdf"


def get_presigned_url(api_url: str, file_path: str):
    response = requests.post(api_url, json={"filename": file_path})
    response.raise_for_status()
    presigned_url = response.json()["url"]["url"]
    fields = response.json()["url"]["fields"]
    return presigned_url, fields


def upload_file_to_s3(
    presigned_url: str, fields: dict[str, Any], file_path: str
) -> None:
    # TODO: perform file size checks
    with open(file_path, "rb") as file:
        files = {"file": (file_path, file)}
        response = requests.post(presigned_url, data=fields, files=files)

    response.raise_for_status()


def main() -> None:
    url, fields = get_presigned_url(api_url, file_path)
    print("Presigned S3 url generated.")

    if not Path(file_path).exists():
        print(f"Error: file not found: {file_path}")
        return
    upload_file_to_s3(url, fields, file_path=file_path)
    print("File uploaded successfully")


if __name__ == "__main__":
    main()
