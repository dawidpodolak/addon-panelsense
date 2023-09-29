from homeassistant.model.ha_outcome_message import HaOutcomeMessage
from mediator.components.light.light_model import LightModel
from pydantic import BaseModel
from server.model.light import ServerMessage


class BaseComponent():
    entity_id: str

    def getHomeAssistantMessage(self) -> HaOutcomeMessage:
        pass

    def getSenseServerMessage(self) -> ServerMessage:
        pass
