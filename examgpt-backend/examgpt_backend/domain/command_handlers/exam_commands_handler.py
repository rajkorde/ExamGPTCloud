import base64
from pathlib import Path
from typing import Optional

from domain.commands.exam_commands import (
    GetExam,
    NotifyUserExamReady,
    NotifyValidateExam,
    SaveExam,
    UpdateExamState,
)
from domain.model.core.exam import Exam
from domain.model.utils.logging import app_logger
from domain.ports.data_service import ExamService
from domain.ports.notification_service import (
    EmailNotificationService,
    ValidationNotificationService,
)
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


def _embed_image(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded_string}"


def _generate_email(exam_code: str, bot_link: str) -> str:
    template_dir = Path(__file__).resolve().parent.parent.parent / "assets"
    logger.debug(f"{template_dir=}")
    env = Environment(loader=FileSystemLoader(str(template_dir)))

    ios_qr_embedded = _embed_image(str(Path(template_dir) / "Telegram_Apple.png"))
    android_qr_embedded = _embed_image(str(Path(template_dir) / "Telegram_Google.png"))

    # Load the template
    template = env.get_template("exam_ready.html")

    # Render the template with the provided data
    output = template.render(
        exam_code=exam_code,
        bot_link=bot_link,
        ios_qr_code=ios_qr_embedded,
        android_qr_code=android_qr_embedded,
    )

    return output


def notify_user_exam_ready(
    command: NotifyUserExamReady, email_service: EmailNotificationService
) -> bool:
    exam_code = NotifyUserExamReady.exam_code
    bot_link = NotifyUserExamReady.bot_link

    subject = "Your exam is ready!"
    body = _generate_email(exam_code, bot_link)
    return email_service.send_notification(
        email=command.email, subject=subject, body=body
    )
