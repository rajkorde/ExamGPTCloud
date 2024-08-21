import json
import os
from typing import Any

from adapter.aws.content_service_s3 import ContentServiceS3
from adapter.aws.environment_service_ssm import EnvironmentServiceSSM
from adapter.aws.exam_service_dynamodb import ExamServiceDynamoDB
from domain.model.utils.exceptions import InvalidEnvironmentSetup
from domain.model.utils.logging import app_logger
from domain.ports.content_service import ContentService
from domain.ports.environment_service import EnvironmentService
from domain.ports.exam_service import ExamService

logger = app_logger.get_logger()


def get_error(
    message: str = "Something went wrong!", error_code: int = 500
) -> dict[str, Any]:
    return {
        "statusCode": error_code,
        "body": json.dumps(
            {
                "message": message,
            }
        ),
    }


class CommandRegistry:
    _command_registry = {
        "AWS": {
            "ContenService": ContentServiceS3,
            "ExamService": ExamServiceDynamoDB,
            "EnvironmentService": EnvironmentServiceSSM,
        }
    }

    def __init__(self):
        self.location = os.getenv("LOCATION")
        if not self.location:
            logger.error("No Environment Variable found: LOCATION")
            raise InvalidEnvironmentSetup(var="LOCATION")

    def get_content_service(self) -> ContentService:
        service = CommandRegistry._command_registry[str(self.location)][
            "ContenService"
        ]()
        assert isinstance(service, ContentService)
        return service

    def get_exam_service(self) -> ExamService:
        service = CommandRegistry._command_registry[str(self.location)]["ExamService"]()
        assert isinstance(service, ExamService)
        return service

    def get_environment_service(self) -> EnvironmentService:
        service = CommandRegistry._command_registry[str(self.location)][
            "EnvironmentService"
        ]()
        assert isinstance(service, EnvironmentService)
        return service
