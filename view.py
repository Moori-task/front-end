from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from credentials import bot_token

import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hi. How can I search for you?")


CAPACITY, RATE, AREA = range(3)


async def automatic_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "در این دستور معیارهای جستجو را خود به شما عرضه می‌کنیم."
        "در هر زمان، برای لغو این عملیات از دستور /cancel استفاده کنید."
        "اقامتگاه شما باید چند نفر ظرفیت داشته‌باشد؟",
    )
    return CAPACITY


async def automatic_search_capacity(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await update.message.reply_text("امتیاز اقامتگاه از چند به بالا باشد مناسب است؟")
    return RATE


async def automatic_search_rate(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await update.message.reply_text("خانه بین چند متر باید باشد؟")
    return AREA


async def automatic_search_area(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    await update.message.reply_text("خدمت شما!")
    return ConversationHandler.END


async def automatic_search_cancel(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "عملیات لغو شد", 
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

automatic_search_handler = ConversationHandler(
    entry_points=[CommandHandler("search_automatic", automatic_search)],
    states={
        CAPACITY: [MessageHandler(filters.Regex("^[1-9][0-9]*$"), automatic_search_capacity)],
        # you should include 0 in rate, too
        RATE: [MessageHandler(filters.Regex("^[1-9][0-9]*$"), automatic_search_rate)],
        AREA: [MessageHandler(filters.Regex("^[1-9][0-9]*$"), automatic_search_area)],
    },
    fallbacks=[CommandHandler("cancel", automatic_search_cancel)],
)

app = ApplicationBuilder().token(bot_token).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(automatic_search_handler)

app.run_polling(poll_interval=0.5)
