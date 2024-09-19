from abc import ABC, abstractmethod


class EmailService(ABC):
    @abstractmethod
    def send_email(self, sender: str, recipient: str, subject: str, body: str) -> bool:
        return True
