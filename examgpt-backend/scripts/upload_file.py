from typing import Any

import requests

api_url = "https://aer2di0h2m.execute-api.us-west-2.amazonaws.com/Stage/upload"


def get_presigned_url(api_url: str, payload: dict[str, Any]) -> str:
    response = requests.post(api_url, json=payload)
    response.raise_for_status()
    presigned_url = response.json().get("url")
    return presigned_url


def main() -> None:
    url = get_presigned_url(api_url, payload={})
    print(f"Presigned Url: {url}")


if __name__ == "__main__":
    main()
