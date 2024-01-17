from telegram import Update
from telegram.ext import (
    BaseHandler,
    CommandHandler,
    ContextTypes,
)

from view.handlers.abstract_handler import AbstractHandler


class StartHandler(AbstractHandler):
    def get_handler(self, command: str) -> BaseHandler:
        return CommandHandler(command, self.handle_start)

    async def handle_start(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        await update.message.reply_text(f"سلام. \n چطور می‌تونم کمکتون کنم؟ ")
