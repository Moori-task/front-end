import json
from typing import List
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    BaseHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import httpx

from debugger import Debugger
from .abstract_view import AbstractView
import pprint


class AutomaticSearchController:
    def __init__(self):
        self.capacity = 0
        self.rate__gte = 0
        self.area__lte = 0
        self.area__gte = 0
        self.reserve_date_before = ""
        self.reserve_date_after = ""

    def set_capacity(self, capacity):
        self.capacity = capacity

    def set_min_rate(self, min_rate):
        self.rate__gte = min_rate

    def set_min_area_size(self, min_area_size):
        self.area__gte = min_area_size

    def set_max_area_size(self, max_area_size):
        self.area__lte = max_area_size

    def set_min_reserve_date(self, min_reserve_date):
        self.reserve_date_after = min_reserve_date

    def set_max_reserve_date(self, max_reserve_date):
        self.reserve_date_before = max_reserve_date

    base_url = "http://127.0.0.1:8080/"
    get_places_offset = "api/place/get/"

    def get_params(self):
        return self.__dict__

    @classmethod
    def parse_json_bytes(cls, b):
        parsed = b.decode("utf-8")
        return json.loads(parsed)

    def get_places(self) -> List:
        with httpx.Client() as client:
            response = client.get(
                url=self.base_url + self.get_places_offset, params=self.get_params()
            )
        return self.parse_json_bytes(response.content)


from enum import Enum, auto, unique

@unique
class AutomaticSearchMenuState(Enum):
    CAPACITY = auto()
    RATE = auto()
    AREA_MIN = auto()
    AREA_MAX = auto()


class AutomaticSearchView(AbstractView):
    def __init__(self):
        self.controller = AutomaticSearchController()

    def get_handler(self, command: str) -> "BaseHandler":
        return ConversationHandler(
            entry_points=[CommandHandler(command, self.handle_start)],
            states={
                AutomaticSearchMenuState.CAPACITY: [
                    MessageHandler(filters.Regex("^[1-9][0-9]*$"), self.handle_capacity)
                ],
                # you should include 0 in rate, too
                AutomaticSearchMenuState.RATE: [
                    MessageHandler(filters.Regex("^[1-9][0-9]*$"), self.handle_rate)
                ],
                # this should be a regex of range. for example, "1-125"
                AutomaticSearchMenuState.AREA_MIN: [
                    MessageHandler(filters.Regex("^[1-9][0-9]*$"), self.handle_area_min)
                ],
                AutomaticSearchMenuState.AREA_MAX: [
                    MessageHandler(filters.Regex("^[1-9][0-9]*$"), self.handle_area_max)
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
        return AutomaticSearchMenuState.CAPACITY

    async def handle_capacity(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        self.controller.set_capacity(int(update.message.text))
        await update.message.reply_text(
            "امتیاز اقامتگاه از چند به بالا باشد مناسب است؟"
        )
        return AutomaticSearchMenuState.RATE

    async def handle_rate(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        self.controller.set_min_rate(int(update.message.text))
        await update.message.reply_text("خانه حداقل چند متر باید باشد؟")
        return AutomaticSearchMenuState.AREA_MIN

    async def handle_area_min(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        self.controller.set_min_area_size(int(update.message.text))
        await update.message.reply_text("خانه حداکثر چند متر باید باشد؟")
        return AutomaticSearchMenuState.AREA_MAX

    def make_pretty(self, item) -> str:
        return pprint.pformat(item)

    async def handle_area_max(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        self.controller.set_max_area_size(int(update.message.text))
        places = self.controller.get_places()
        await update.message.reply_text("خدمت شما!\n" + self.make_pretty(places))
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
