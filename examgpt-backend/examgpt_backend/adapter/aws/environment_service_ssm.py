from typing import Optional

import boto3
from domain.model.utils.logging import app_logger
from domain.ports.environment_service import EnvironmentService

logger = app_logger.get_logger()


class EnvironmentServiceSSM(EnvironmentService):
    def __init__(self):
        self.ssm = boto3.client("ssm")

    def get_parameter(self, name: str, is_encrypted: bool = False) -> Optional[str]:
        try:
            response = self.ssm.get_parameter(Name=name, WithDecryption=is_encrypted)
            return str(response["Parameter"]["Value"])
        except self.ssm.exceptions.ParameterNotFound:
            logger.error(f"The parameter {name} was not found.")
            return None
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return None
