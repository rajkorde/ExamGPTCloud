import json

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from domain.model.utils.exceptions import InvalidEnvironmentSetup
from domain.model.utils.logging import app_logger
from domain.model.utils.misc import get_env_var
from domain.ports.notification_service import ChunkNotificationService

logger = app_logger.get_logger()


class ChunkNotificationServiceSNS(ChunkNotificationService):
    def __init__(self):
        SNS_TOPIC_ENV_VAR: str = "CHUNK_TOPIC"
        self.topic_name = get_env_var(SNS_TOPIC_ENV_VAR)
        if not self.topic_name:
            raise InvalidEnvironmentSetup(SNS_TOPIC_ENV_VAR)
        self.sns = boto3.client("sns")

    def send_notification(self, chunk_ids: list[str]) -> bool:
        message = {"default": json.dumps({"chunk_ids": chunk_ids})}

        try:
            self.sns.publish(
                TopicArn=self.topic_name,
                Message=json.dumps(message),
                MessageStructure="json",
            )
        except (BotoCoreError, ClientError) as e:
            logger.error(
                f"Failed to send notification to topic: {self.topic_name}: {e}"
            )
            return False
        return True
