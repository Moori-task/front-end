from typing import Dict, List
from telegram.ext import ApplicationBuilder
from .credentials import bot_token

from .handlers import AbstractHandler, AutomaticSearchHandler, StartHandler


class MainView:
    def __init__(self) -> None:
        self.app = ApplicationBuilder().token(bot_token).build()
        self.handlers: Dict[str, "AbstractHandler"] = {
            'start': StartHandler(),
            'search_automatic': AutomaticSearchHandler()
        }
        self.register_handlers()

    def register_handlers(self):
        for command, handler in self.handlers.items():
            self.app.add_handler(handler.get_handler(command))

    def run(self):
        self.app.run_polling()
