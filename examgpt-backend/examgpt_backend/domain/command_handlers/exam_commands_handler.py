from typing import Optional

from domain.commands.exam_commands import GetExam, SaveExam, UpdateExamState
from domain.model.core.exam import Exam
from domain.ports.data_service import ExamService


def save_exam(command: SaveExam, exam_service: ExamService) -> bool:
    return exam_service.put_exam(command.exam)


def update_exam_state(command: UpdateExamState, exam_service: ExamService) -> bool:
    return exam_service.update_state(
        exam_code=command.exam_code, newstate=command.state
    )


def get_exam(command: GetExam, exam_service: ExamService) -> Optional[Exam]:
    return exam_service.get_exam(exam_code=command.exam_code)
