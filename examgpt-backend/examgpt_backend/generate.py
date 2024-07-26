import json
from typing import Any


def handler(event: dict[str, Any], context: Any):
    message = "Generating QAs based on messages"
    print(message)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": message,
            }
        ),
    }
