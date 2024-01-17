from telegram.ext import (
    ApplicationBuilder
)
from .credentials import bot_token

from .handlers import AutomaticSearchView, start_handler

class MainView:
    def __init__(self) -> None:
        self.app = ApplicationBuilder().token(bot_token).build()
        self.register_handlers()
    
    def register_handlers(self):
        self.app.add_handler(start_handler)
        self.app.add_handler(AutomaticSearchView().get_handler())

    def run(self):
        self.app.run_polling()
