from pydantic import BaseModel
from mediator.components.light.light_model import LightModel
from homeassistant.model.ha_outcome_message import HaOutcomeMessage


class BaseComponent():
    entity_id: str

    def getHomeAssistantMessage(self) -> HaOutcomeMessage:
        pass

    def getSenseServerMessage(self) -> LightModel:
        pass
