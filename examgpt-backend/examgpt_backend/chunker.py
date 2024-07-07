import json
from typing import Any


def handler(event: dict[str, Any], context: Any):
    message = "In Chunking code"
    print(f"{event=}")
    print(f"{message=}")

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": message,
            }
        ),
    }
