from mediator.components.light.light_state import LightState
from pydantic import BaseModel
from server.model.light import ServerMessage


class LightModel(ServerMessage):
    entity_id: str
    state: LightState
