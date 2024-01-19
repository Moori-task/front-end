from debugger import Debugger
from views.automatic_search_abstracts import TraversingState
from .automatic_search_abstracts import SingleTransitionState, StateTransition

from typing import List, Type
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    BaseHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import pprint

class CapacityState(SingleTransitionState):
    id = 0
    async def run(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "اقامتگاه شما باید چند نفر ظرفیت داشته‌باشد؟",
        )

    class Transition(StateTransition):
        def next_state(self):
            return RateState(self.controller)

        async def run(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
            self.controller.set_capacity(int(update.message.text))

        def get_handler(self):
            return MessageHandler(filters.Regex("^[1-9][0-9]*$"), self.handle)


class RateState(SingleTransitionState):
    id = 1
    async def run(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "امتیاز اقامتگاه از چند به بالا باشد مناسب است؟"
        )

    class Transition(StateTransition):
        def next_state(self):
            return AreaMinState(self.controller)

        async def run(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
            self.controller.set_min_rate(int(update.message.text))

        def get_handler(self):
            # you should include 0 in rate, too
            return MessageHandler(filters.Regex("^[1-9][0-9]*$"), self.handle)
        
class AreaMinState(SingleTransitionState):
    id = 2
    async def run(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("خانه حداقل چند متر باید باشد؟")

    class Transition(StateTransition):
        def next_state(self):
            return AreaMaxState(self.controller)

        async def run(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
            self.controller.set_min_area_size(int(update.message.text))

        def get_handler(self):
            return MessageHandler(filters.Regex("^[1-9][0-9]*$"), self.handle)
        
class AreaMaxState(SingleTransitionState):
    id = 3
    async def run(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("خانه حداقل چند متر باید باشد؟")

    class Transition(StateTransition):
        def next_state(self):
            return AreaMaxState(self.controller)

        def get_handler(self):
            return MessageHandler(filters.Regex("^[1-9][0-9]*$"), self.handle)

        def make_pretty(self, item) -> str:
            return pprint.pformat(item)
        
        async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
            self.controller.set_max_area_size(int(update.message.text))
            places = self.controller.get_places()
            await update.message.reply_text("خدمت شما!\n" + self.make_pretty(places))
            return ConversationHandler.END
        
        # TODO refused bequest
        async def run(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
            return await super().run(update, context)
        


class StartTransition(StateTransition):
    def get_handler(self):
        return CommandHandler("search_automatic", self.handle)

    async def run(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "در این دستور معیارهای جستجو را خود به شما عرضه می‌کنیم.\n"
            "در هر زمان، برای لغو این عملیات از دستور /cancel استفاده کنید.\n"
        )

    def next_state(self):
        return CapacityState(self.controller)
    

class CancelTransition(StateTransition):
    def get_handler(self):
        return CommandHandler("cancel", self.handle)

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        Debugger().get_logger().info(
            "User %s canceled the conversation.", user.first_name
        )
        await update.message.reply_text(
            "عملیات لغو شد", reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    

    # TODO: handle refused bequest
    async def run(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        return await super().run(update, context)
    
    def next_state(self) -> TraversingState:
        return super().next_state()