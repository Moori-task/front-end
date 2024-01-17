#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import asyncio
import logging

from telegram import Bot, ForceReply, Update
import telegram
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from credentials import bot_token

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx")

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    print("jesus")
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )
    print("jesus2")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    print("aaaaah")
    await update.message.reply_text(update.message.text)


async def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    # b_proxy = 'http://192.168.43.1:18009'
    # application = ApplicationBuilder().proxy(b_proxy).token(bot_token).build()
    application = ApplicationBuilder().token(bot_token).build()
    # await application.bot.request.post('https://www.youtube.com')
    bot: Bot = application.bot
    # k = await bot._request[0].post(url="https://api.telegram.org/bot6484830100:AAG9itC_ZgVbLvmAVvK6oVb3HLi8tC4DRlE/getUpdates")
    k = await bot.get_updates()
    # k = await bot.get_updates(connect_timeout=2000000,
    #         read_timeout=200000,
    #         write_timeout=2000000,
    #         pool_timeout=20000)
    print(k)
    # print(k)
    # # on different commands - answer in Telegram
    # application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("help", help_command))

    # # on non command i.e message - echo the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # # Run the bot until the user presses Ctrl-C
    # application.run_polling(allowed_updates=Update.ALL_TYPES, poll_interval=0.5)
    # await application.bot.send_message(chat_id='69887066', text='hi')


if __name__ == "__main__":
    asyncio.run(main())