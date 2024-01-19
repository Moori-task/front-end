from abc import ABC, abstractmethod

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


class TraversingState(ABC):
    id: int

    def __init__(self, controller):
        self.controller = controller

    @abstractmethod
    async def run(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass

    @abstractmethod
    def get_handlers(self) -> List["StateTransition"]:
        pass


class SingleTransitionState(TraversingState):
    Transition: Type["StateTransition"]

    def get_handlers(self) -> List["StateTransition"]:
        return [self.Transition(self.controller)]


class StateTransition(ABC):
    def __init__(self, controller):
        self.controller = controller

    @abstractmethod
    def get_handler(self) -> "BaseHandler":
        pass

    @abstractmethod
    async def run(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass

    @abstractmethod
    def next_state(self) -> "TraversingState":
        pass

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.run(update, context)
        await self.next_state().run(update, context)
        return self.next_state().id
