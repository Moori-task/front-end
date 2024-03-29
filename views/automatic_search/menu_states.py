from debugger import Debugger
from .menu_state_abstracts import TraversingState
from .menu_state_abstracts import SingleTransitionState, StateTransition

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import pprint


DATE_REGEX = r"^(19|20)\d{2}-(0[1-9]|1[1,2])-(0[1-9]|[12][0-9]|3[01])$"
INT_REGEX = r"^[1-9][0-9]*$"
# TODO: Obvious :)
FLOAT_REGEX = INT_REGEX
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
            return MessageHandler(filters.Regex(INT_REGEX), self.handle)


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
            return MessageHandler(filters.Regex(FLOAT_REGEX), self.handle)
        
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
            return MessageHandler(filters.Regex(INT_REGEX), self.handle)
        
class AreaMaxState(SingleTransitionState):
    id = 3
    async def run(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("خانه حداقل چند متر باید باشد؟")

    class Transition(StateTransition):
        def get_handler(self):
            return MessageHandler(filters.Regex(INT_REGEX), self.handle)
        
        def next_state(self) -> "TraversingState":
            return ReserveMinDateState(self.controller)
        
        async def run(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
            self.controller.set_max_area_size(int(update.message.text))

class ReserveMinDateState(SingleTransitionState):
    id = 4
    async def run(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("از چه تاریخی می‌خواهید رزرو انجام دهید؟")

    class Transition(StateTransition):
        def get_handler(self):
            return MessageHandler(filters.Regex(DATE_REGEX), self.handle)
        
        def next_state(self) -> "TraversingState":
            return ReserveMaxDateState(self.controller)
        
        async def run(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
            self.controller.set_min_reserve_date(str(update.message.text))

class ReserveMaxDateState(SingleTransitionState):
    id = 5
    async def run(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("تا چه تاریخی می‌خواهید رزرو انجام دهید؟")

    class Transition(StateTransition):
        def get_handler(self):
            return MessageHandler(filters.Regex(DATE_REGEX), self.handle)

        def make_pretty(self, item) -> str:
            return pprint.pformat(item)
        
        async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
            self.controller.set_max_reserve_date(str(update.message.text))
            places = self.controller.get_places()
            await update.message.reply_text("خدمت شما!\n" + self.make_pretty(places))
            return ConversationHandler.END
        
        # TODO refused bequest
        def next_state(self) -> "TraversingState":
            return super().next_state()
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