from pydantic import BaseModel
from mediator.components.light.state import LightState


class LightModel(BaseModel):
    entity_id: str
    state: LightState
