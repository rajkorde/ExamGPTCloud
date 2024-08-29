from domain.commands.exam_commands import SaveExam, UpdateExamState
from domain.ports.data_service import ExamService


def save_exam(command: SaveExam, exam_service: ExamService) -> bool:
    return exam_service.put_exam(command.exam)


def update_exam_state(command: UpdateExamState, exam_service: ExamService) -> bool:
    return exam_service.update_state(
        exam_code=command.exam_code, newstate=command.state
    )
