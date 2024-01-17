from typing import Dict, List
from telegram.ext import ApplicationBuilder
from .credentials import bot_token

from .views import AbstractView, AutomaticSearchView, StartView


class ViewConfig:
    def __init__(self) -> None:
        self.app = ApplicationBuilder().token(bot_token).build()
        self.views: Dict[str, "AbstractView"] = {
            "start": StartView(),
            "search_automatic": AutomaticSearchView(),
        }
        self.register_handlers()

    def register_handlers(self):
        for command, handler in self.views.items():
            self.app.add_handler(handler.get_handler(command))

    def run(self):
        self.app.run_polling()
