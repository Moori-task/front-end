from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hi. How can I search for you?")

start_handler = CommandHandler("start", start)