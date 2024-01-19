from typing import List
from telegram.ext import (
    BaseHandler,
    ConversationHandler,
)

from .menu_state_abstracts import StateTransition, TraversingState
from .menu_states import AreaMaxState, AreaMinState, CancelTransition, CapacityState, RateState, StartTransition
from ..abstract_view import AbstractView
from .controller import AutomaticSearchController

class AutomaticSearchView(AbstractView):
    def __init__(self):
        self.controller = AutomaticSearchController()

    def get_handler(self, command: str) -> "BaseHandler":
        def transform_handlers(handlers: List[StateTransition]):
            return list(map(lambda transition: transition.get_handler(), handlers))
            
        start_transitions: List["StateTransition"] = [StartTransition(self.controller)]
        entry_points = transform_handlers(start_transitions)

        menu_states: List["TraversingState"] = [
            CapacityState(self.controller),
            RateState(self.controller),
            AreaMinState(self.controller),
            AreaMaxState(self.controller),
        ]
        # TODO replace loops with pipelines
        # TODO state_id
        states = {}
        for menu_state in menu_states:
            states[menu_state.id] = transform_handlers(menu_state.get_handlers())

        cancel_transitions: List["StateTransition"] = [CancelTransition(self.controller)]
        fallbacks=transform_handlers(cancel_transitions)
        
        # TODO watch over fallback types
        return ConversationHandler(
            entry_points=entry_points,
            states=states,
            fallbacks=fallbacks,
        )