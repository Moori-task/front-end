from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from credentials import bot_token

from automatic_search import AutomaticSearchView



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hi. How can I search for you?")


app = ApplicationBuilder().token(bot_token).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(AutomaticSearchView().get_handler())

app.run_polling()
