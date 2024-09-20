from typing import Optional

from domain.commands.work_tracker_commands import (
    AddExamTracker,
    GetExamTracker,
    IncrementCompletedWorkers,
    ResetExamTracker,
    UpdateTotalWorkers,
)
from domain.model.utils.work_tracker import WorkTracker
from domain.ports.data_service import WorkTrackerService


def add_exam_tracker(
    command: AddExamTracker, work_tracker_service: WorkTrackerService
) -> bool:
    return work_tracker_service.add_exam_tracker(exam_code=command.exam_code)


def get_exam_tracker(
    command: GetExamTracker, work_tracker_service: WorkTrackerService
) -> Optional[WorkTracker]:
    return work_tracker_service.get_exam_tracker(exam_code=command.exam_code)


def reset_exam_tracker(
    command: ResetExamTracker, work_tracker_service: WorkTrackerService
) -> bool:
    return work_tracker_service.reset_exam_tracker(exam_code=command.exam_code)


def update_total_workers(
    command: UpdateTotalWorkers, work_tracker_service: WorkTrackerService
) -> bool:
    return work_tracker_service.update_total_workers(
        exam_code=command.exam_code, total_workers=command.total_workers
    )


def increment_completed_workers(
    command: IncrementCompletedWorkers, work_tracker_service: WorkTrackerService
) -> bool:
    return work_tracker_service.increment_completed_workers(exam_code=command.exam_code)
