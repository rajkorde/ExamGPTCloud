import os
from typing import Any

import boto3
from dotenv import load_dotenv

env_file = "examgpt_backend/.env"


def get_ssm_parameters() -> list[Any]:
    ssm = boto3.client("ssm")
    parameters = []
    next_token = None

    while True:
        if next_token:
            response = ssm.describe_parameters(
                ParameterFilters=[
                    {"Key": "Name", "Option": "Contains", "Values": ["examgpt"]}
                ],
                NextToken=next_token,
                MaxResults=50,
            )
        else:
            response = ssm.describe_parameters(
                ParameterFilters=[
                    {"Key": "Name", "Option": "Contains", "Values": ["examgpt"]}
                ],
                MaxResults=50,
            )

        parameters.extend(response["Parameters"])

        if "NextToken" not in response:
            break
        next_token = response["NextToken"]

    return parameters


def get_parameter_value(name: str) -> str:
    ssm = boto3.client("ssm")
    response = ssm.get_parameter(Name=name, WithDecryption=True)
    return response["Parameter"]["Value"]


def update_parameter(name: str, value: str):
    ssm = boto3.client("ssm")
    try:
        ssm.put_parameter(Name=name, Value=value, Type="SecureString", Overwrite=True)
        print(f"Updated parameter: {name}")
    except Exception as e:
        print(f"Error updating parameter {name}: {str(e)}")


def main():
    assert load_dotenv(
        dotenv_path=env_file
    ), f"The path to env file is incorrect: {env_file}"

    ssm_parameters = get_ssm_parameters()

    param = ssm_parameters[0]

    for param in ssm_parameters:
        param_name = param["Name"]
        # Assume the env var name is the last part of the parameter name
        env_var_name = param_name.split("/")[-1]

        # Check if the parameter exists in .env
        if env_var_name in os.environ:
            current_value = get_parameter_value(param_name)
            env_value = os.environ[env_var_name]

            # If values are different, update SSM
            if current_value != env_value:
                update_parameter(param_name, env_value)
            else:
                print(f"No update needed for {param_name}")
        else:
            print(f"No matching .env variable found for {param_name}")


if __name__ == "__main__":
    main()
