from pydantic import BaseModel
from typing import Optional, List


class ServerMessage(BaseModel):
    entity_id: str


class LightState(BaseModel):
    on: bool = False
    brightness: int = 0,
    color_mode: Optional[str] = None
    rgb_color: Optional[List[int]] = None
    color_temp_kelvin: Optional[int] = None


class LightMessage(ServerMessage):
    entity_id: str
    state: LightState
