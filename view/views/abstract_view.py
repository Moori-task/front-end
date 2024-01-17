from abc import ABC, abstractmethod
from telegram.ext import BaseHandler


class AbstractView(ABC):
    @abstractmethod
    def get_handler(self, command: str) -> "BaseHandler":
        pass
