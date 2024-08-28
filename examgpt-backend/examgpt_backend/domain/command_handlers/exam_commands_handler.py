from domain.commands.exam_commands import SaveExam
from domain.ports.data_service import ExamService


def save_exam(command: SaveExam, exam_service: ExamService) -> bool:
    return exam_service.put_exam(command.exam)
