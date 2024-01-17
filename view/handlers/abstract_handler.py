from abc import ABC, abstractmethod
from telegram.ext import BaseHandler


class AbstractHandler(ABC):
    def __init__(self, command: str):
        self.command = command

    @abstractmethod
    def get_handler(self) -> "BaseHandler":
        pass
