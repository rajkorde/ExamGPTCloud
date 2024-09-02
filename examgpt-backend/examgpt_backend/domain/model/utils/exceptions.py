class BaseException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class InvalidEnvironmentSetup(BaseException):
    """Raised when the right environment variables are not found"""

    def __init__(self, var: str):
        message: str = (
            f"Invalid Environment setup. Could not find environment variable: {var}"
        )
        super().__init__(message=message)


class ExamAlreadyExists(BaseException):
    """Raised when exam to be created already exists"""

    def __init__(self, var: str):
        message: str = f"Exam already exists: {var}"
        super().__init__(message=message)


class InvalidExam(BaseException):
    """Raised when there is no exam code in exam"""

    def __init__(self):
        message: str = "Exam does not have exam code."
        super().__init__(message=message)


class PromptNotFound(BaseException):
    """Raised when prompt for a scenario is not found"""

    def __init__(self, message: str = "Prompt not found"):
        super().__init__(message=message)


class NotEnoughInformationInContext(BaseException):
    """Raised when provided text chunk does not have enough information to create a question"""

    def __init__(
        self,
        chunk_id: str,
    ):
        message: str = f"Text chunk does not have enough information to create a question: {chunk_id}"
        super().__init__(message=message)


class NotEnoughQuestionsInExam(BaseException):
    """Raised when there are not enough questions in an exam"""

    def __init__(self, exam_code: str):
        message: str = f"Not enough questions in exam: {exam_code}"
        super().__init__(message=message)
