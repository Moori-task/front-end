from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"سلام. \n چطور می‌تونم کمکتون کنم؟ ")

start_handler = CommandHandler("start", start)