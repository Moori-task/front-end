from abc import ABC, abstractmethod
from telegram.ext import BaseHandler


class AbstractHandler(ABC):
    @abstractmethod
    def get_handler(self, command: str) -> "BaseHandler":
        pass
