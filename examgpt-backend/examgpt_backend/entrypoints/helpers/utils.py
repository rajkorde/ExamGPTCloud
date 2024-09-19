import json
import os
from typing import Any

from adapter.ai.ai_service_ext import AIServiceExt
from adapter.ai.model_providers.openai import OpenAIProvider
from adapter.aws.content_service_s3 import ContentServiceS3
from adapter.aws.data_service_dynamodb import (
    ChunkServiceDynamoDB,
    ExamServiceDynamoDB,
    QAServiceDynamodb,
)
from adapter.aws.email_service_ses import EmailServiceSES
from adapter.aws.environment_service_ssm import EnvironmentServiceSSM
from adapter.aws.notification_service_sns import (
    ChunkNotificationServiceSNS,
    ValidationNotificationServiceSNS,
)
from domain.ai.base import BaseModelProvider
from domain.model.utils.exceptions import InvalidEnvironmentSetup
from domain.model.utils.logging import app_logger
from domain.ports.ai_service import AIService
from domain.ports.content_service import ContentService
from domain.ports.data_service import ChunkService, ExamService, QAService
from domain.ports.email_service import EmailService
from domain.ports.environment_service import EnvironmentService
from domain.ports.notification_service import (
    ChunkNotificationService,
    ValidationNotificationService,
)

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


def get_success(message: str = "OK") -> dict[str, Any]:
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "OK",
            }
        ),
    }


class CommandRegistry:
    _command_registry = {
        "AWS": {
            "ContentService": ContentServiceS3,
            "ExamService": ExamServiceDynamoDB,
            "EnvironmentService": EnvironmentServiceSSM,
            "ChunkService": ChunkServiceDynamoDB,
            "ChunkNotificationService": ChunkNotificationServiceSNS,
            "AIService": AIServiceExt,
            "ModelProvider": OpenAIProvider,
            "QAService": QAServiceDynamodb,
            "ValidationNotificationService": ValidationNotificationServiceSNS,
            "EmailService": EmailServiceSES,
        }
    }

    def __init__(self):
        self.location = os.getenv("LOCATION")
        if not self.location:
            logger.error("No Environment Variable found: LOCATION")
            raise InvalidEnvironmentSetup(var="LOCATION")

    def get_content_service(self) -> ContentService:
        service = CommandRegistry._command_registry[str(self.location)][
            "ContentService"
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

    def get_chunk_service(self) -> ChunkService:
        service = CommandRegistry._command_registry[str(self.location)][
            "ChunkService"
        ]()
        assert isinstance(service, ChunkService)
        return service

    def get_chunk_notification_service(self) -> ChunkNotificationService:
        service = CommandRegistry._command_registry[str(self.location)][
            "ChunkNotificationService"
        ]()
        assert isinstance(service, ChunkNotificationService)
        return service

    def get_ai_service(self) -> AIService:
        service = CommandRegistry._command_registry[str(self.location)]["AIService"]()
        assert isinstance(service, AIService)
        return service

    def get_model_provider(self) -> BaseModelProvider:
        model_provider = CommandRegistry._command_registry[str(self.location)][
            "ModelProvider"
        ]()
        assert isinstance(model_provider, BaseModelProvider)
        return model_provider

    def get_qa_service(self) -> QAService:
        service = CommandRegistry._command_registry[str(self.location)]["QAService"]()
        assert isinstance(service, QAService)
        return service

    def get_validation_notification_service(self) -> ValidationNotificationService:
        service = CommandRegistry._command_registry[str(self.location)][
            "ValidationNotificationService"
        ]()
        assert isinstance(service, ValidationNotificationService)
        return service

    def get_email_service(self) -> EmailService:
        service = CommandRegistry._command_registry[str(self.location)][
            "EmailService"
        ]()
        assert isinstance(service, EmailService)
        return service
