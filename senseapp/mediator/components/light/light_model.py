from pydantic import BaseModel
from mediator.components.light.light_state import LightState


class LightModel(BaseModel):
    entity_id: str
    state: LightState
