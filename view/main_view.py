from typing import List
from telegram.ext import ApplicationBuilder
from .credentials import bot_token

from .handlers import AbstractHandler, AutomaticSearchHandler, StartHandler


class MainView:
    def __init__(self) -> None:
        self.app = ApplicationBuilder().token(bot_token).build()
        self.handlers: List[AbstractHandler] = [StartHandler('start'), AutomaticSearchHandler('search_automatic')]
        self.register_handlers()

    def register_handlers(self):
        map(lambda handler: self.app.add_handler(handler.get_handler()), self.handlers)

    def run(self):
        self.app.run_polling()
