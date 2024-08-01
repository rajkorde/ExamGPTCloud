import json
from typing import Any

import boto3

ssm = boto3.client("ssm")
openai_key_name = "/examgpt/OPENAI_API_KEY"


def get_parameter(parameter_name: str, with_decryption: bool = True):
    try:
        response = ssm.get_parameter(
            Name=parameter_name, WithDecryption=with_decryption
        )
        return str(response["Parameter"]["Value"])
    except ssm.exceptions.ParameterNotFound:
        print(f"The parameter {parameter_name} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def handler(event: dict[str, Any], context: Any):
    message = "Generating QAs based on messages"
    print(message)
    print(f"{event}")

    key = get_parameter(parameter_name=openai_key_name)
    print(f"{key=}")

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": message,
            }
        ),
    }
