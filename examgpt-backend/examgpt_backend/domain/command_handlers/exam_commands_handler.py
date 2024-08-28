from domain.commands.exam_commands import SaveExam
from domain.ports.data_service import DataService


def save_exam(command: SaveExam, exam_service: DataService) -> bool:
    return exam_service.put_exam(command.exam)
