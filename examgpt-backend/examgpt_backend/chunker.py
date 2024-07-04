import json


def handler(event, context):
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
