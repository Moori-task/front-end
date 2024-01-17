from telegram.ext import (
    ApplicationBuilder
)
from credentials import bot_token

from handlers import AutomaticSearchView, start_handler


app = ApplicationBuilder().token(bot_token).build()

app.add_handler(start_handler)
app.add_handler(AutomaticSearchView().get_handler())

app.run_polling()
