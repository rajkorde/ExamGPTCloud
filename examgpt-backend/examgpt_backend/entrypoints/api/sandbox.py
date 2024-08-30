import json
from typing import Any


def handler(event: dict[Any, Any], context: Any) -> dict[str, Any]:
    print("Executing sandbox.")
    return {
        "statusCode": 200,
        "body": json.dumps({"value": "test"}),
    }
