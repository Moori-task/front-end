from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    BaseHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from debugger import Debugger
from .abstract_view import AbstractView

CAPACITY, RATE, AREA = range(3)

# TODO: Separate data from presentation
class AutomaticSearchView(AbstractView):
    def __init__(self):
        self.capacity = 0
        self.min_rate = 0
        self.area_range = (0, 0)

    def __str__(self) -> str:
        return f"capacity: {self.capacity}, rate: {self.rate}, area: {str(self.area_range)}"

    def get_handler(self, command: str) -> "BaseHandler":
        return ConversationHandler(
            entry_points=[CommandHandler(command, self.handle_start)],
            states={
                CAPACITY: [
                    MessageHandler(filters.Regex("^[1-9][0-9]*$"), self.handle_capacity)
                ],
                # you should include 0 in rate, too
                RATE: [
                    MessageHandler(filters.Regex("^[1-9][0-9]*$"), self.handle_rate)
                ],
                # this should be a regex of range. for example, "1-125"
                AREA: [
                    MessageHandler(filters.Regex("^[1-9][0-9]*$"), self.handle_area)
                ],
            },
            fallbacks=[CommandHandler("cancel", self.handle_cancel)],
        )

    async def handle_start(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        await update.message.reply_text(
            "در این دستور معیارهای جستجو را خود به شما عرضه می‌کنیم.\n"
            "در هر زمان، برای لغو این عملیات از دستور /cancel استفاده کنید.\n"
            "اقامتگاه شما باید چند نفر ظرفیت داشته‌باشد؟",
        )
        return CAPACITY

    async def handle_capacity(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        self.capacity = int(update.message.text)
        await update.message.reply_text(
            "امتیاز اقامتگاه از چند به بالا باشد مناسب است؟"
        )
        return RATE

    async def handle_rate(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        self.rate = int(update.message.text)
        await update.message.reply_text("خانه بین چند متر باید باشد؟")
        return AREA

    async def handle_area(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        self.area_range = (int(update.message.text), int(update.message.text) + 1)
        await update.message.reply_text("خدمت شما!\n" + str(self))
        return ConversationHandler.END

    async def handle_cancel(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Cancels and ends the conversation."""
        user = update.message.from_user
        Debugger().get_logger().info(
            "User %s canceled the conversation.", user.first_name
        )
        await update.message.reply_text(
            "عملیات لغو شد", reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
