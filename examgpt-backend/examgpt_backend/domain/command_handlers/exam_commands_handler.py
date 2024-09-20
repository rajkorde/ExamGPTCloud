from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Optional

from domain.commands.exam_commands import (
    EmailUserExamReady,
    GetExam,
    NotifyValidateExam,
    SaveExam,
    UpdateExamState,
)
from domain.model.core.exam import Exam
from domain.model.utils.logging import app_logger
from domain.ports.data_service import ExamService
from domain.ports.email_service import EmailService
from domain.ports.notification_service import ValidationNotificationService
from jinja2 import Environment, FileSystemLoader

logger = app_logger.get_logger()


def save_exam(command: SaveExam, exam_service: ExamService) -> bool:
    return exam_service.put_exam(command.exam)


def update_exam_state(command: UpdateExamState, exam_service: ExamService) -> bool:
    return exam_service.update_state(
        exam_code=command.exam_code, newstate=command.state
    )


def get_exam(command: GetExam, exam_service: ExamService) -> Optional[Exam]:
    return exam_service.get_exam(exam_code=command.exam_code)


def notify_validate_exam(
    command: NotifyValidateExam, notification_service: ValidationNotificationService
) -> bool:
    return notification_service.send_notification(command.exam_code)


def _generate_email(exam_code: str, bot_link: str) -> str:
    template_dir = Path(__file__).resolve().parent.parent.parent / "assets"
    env = Environment(loader=FileSystemLoader(str(template_dir)))

    # Load the template
    template = env.get_template("exam_ready.html")

    # Render the template with the provided data
    output = template.render(
        exam_code=exam_code,
        bot_link=bot_link,
    )

    return output


def email_user_exam_ready(
    command: EmailUserExamReady, email_service: EmailService
) -> bool:
    sender = "Examiner <examiner@myexamgpt.com>"
    recipient = command.email
    subject = "Your exam is ready!"
    msg = MIMEMultipart("related")

    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    # Create the body of the email (HTML part)
    body = _generate_email(command.exam_code, command.bot_link)
    msg_body = MIMEMultipart("alternative")
    body_html_part = MIMEText(body, "html")
    msg_body.attach(body_html_part)
    msg.attach(msg_body)

    template_dir = Path(__file__).resolve().parent.parent.parent / "assets"

    image_paths = {
        "ios_qr_code": str(Path(template_dir) / "Telegram_Apple.png"),
        "android_qr_code": str(Path(template_dir) / "Telegram_Google.png"),
    }
    for cid, image_path in image_paths.items():
        with open(image_path, "rb") as img:
            img_data = img.read()
            image_part = MIMEImage(img_data)
            image_part.add_header("Content-ID", f"<{cid}>")
            image_part.add_header("Content-Disposition", "inline", filename=image_path)
            msg.attach(image_part)

    return email_service.send_email(sender, recipient, subject, msg.as_string())
