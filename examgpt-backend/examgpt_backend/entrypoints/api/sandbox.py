import json
from typing import Any

from domain.ai.constants import ModelFamily


def handler(event: dict[Any, Any], context: Any) -> dict[str, Any]:
    print("Executing sandbox.")
    print(ModelFamily.GOOGLE.value)
    return {
        "statusCode": 200,
        "body": json.dumps({"value": "test"}),
    }
