from pydantic import BaseModel
from mediator.components.light.light_model import LightModel


class BaseComponent():
    entity_id: str

    def getHassMessage(self):
        pass

    def getSenseServerMessage(self) -> LightModel:
        pass
