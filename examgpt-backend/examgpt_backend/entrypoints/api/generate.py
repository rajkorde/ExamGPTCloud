import json
import os
from typing import Any

import boto3
from domain.model.utils.logging import app_logger

# from ai.model_providers
# logger = app_logger.get_logger()
ssm = boto3.client("ssm")
openai_key_name = "/examgpt/OPENAI_API_KEY"

ddb = boto3.resource("dynamodb")
logger = app_logger.get_logger()


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
    message = "Generating QAs based on notifcation."
    logger.debug(message)
    # print(f"{event}")

    chunk_table = os.environ["CHUNK_TABLE"]
    if not chunk_table:
        logger.error("Error: Could not find chunk table in environment variables")
    logger.debug(f"{chunk_table=}")

    key = get_parameter(parameter_name=openai_key_name)
    keyname = openai_key_name.split("/")[-1]
    if not key:
        logger.error(f"Error: Incorrect key from ssm parameter store: {key}")
    else:
        os.environ[keyname] = key
    logger.debug(f"{key=}")

    chunk = event["Records"][0]["Sns"]["Message"]
    logger.debug(f"{chunk=}")

    # model = OpenAIProvider()
    # chat = model.get_chat_model()

    # messages = [
    #     (
    #         "system",
    #         "You are a helpful assistant that summarizes paragraphs",
    #     ),
    #     ("human", chunk),
    # ]

    # response = chat.invoke(messages)
    # print(response.content)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "OK",
            }
        ),
    }
