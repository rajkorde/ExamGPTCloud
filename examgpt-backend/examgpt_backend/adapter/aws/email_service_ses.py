import boto3
from botocore.exceptions import BotoCoreError, ClientError
from domain.model.utils.logging import app_logger
from domain.ports.email_service import EmailService

logger = app_logger.get_logger()


class EmailServiceSES(EmailService):
    def __init__(self) -> None:
        self.ses = boto3.client("ses")

    def send_email(self, sender: str, recipient: str, subject: str, body: str) -> bool:
        try:
            response = self.ses.send_email(
                Source=sender,
                Destination={
                    "ToAddresses": [recipient],
                },
                Message={
                    "Subject": {"Data": subject, "Charset": "UTF-8"},
                    "Body": {"Html": {"Data": body, "Charset": "UTF-8"}},
                },
            )
            logger.info(f"Email sent! Message ID: {response['MessageId']}")
            return True

        except (BotoCoreError, ClientError) as error:
            print(f"Error occurred: {error}")
            return False
