from homeassistant.model.ha_outcome_message import HaOutcomeMessage
from pydantic import BaseModel
from server.model.base import ServerOutgoingMessage
from server.model.light import ServerMessage


class BaseComponent:
    entity_id: str

    def get_message_for_home_assistant(self) -> HaOutcomeMessage:
        pass

    def get_message_for_client(self) -> ServerOutgoingMessage:
        pass
