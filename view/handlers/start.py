from telegram import Update
from telegram.ext import (
    BaseHandler,
    CommandHandler,
    ContextTypes,
)

from view.handlers.abstract_handler import AbstractHandler


class StartHandler(AbstractHandler):
    def __init__(self, command: str):
        super().__init__(command)

    def get_handler(self) -> BaseHandler:
        return CommandHandler("start", self.handle_start)

    async def handle_start(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        await update.message.reply_text(f"سلام. \n چطور می‌تونم کمکتون کنم؟ ")
