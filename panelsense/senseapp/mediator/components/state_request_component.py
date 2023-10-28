from homeassistant.ids import get_message_id
from homeassistant.model.ha_outcome_message import *

from .base_component import BaseComponent


class StateRequest(BaseComponent):
    def get_message_for_home_assistant(self) -> HaOutcomeMessage:
        return HaOutcomeMessage(id=get_message_id(), type="get_states")
