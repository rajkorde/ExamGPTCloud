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
