from pydantic import BaseModel


class ServerMessage(BaseModel):
    entity_id: str


class LightState(BaseModel):
    on: bool = False
    brightness: int = 0


class LightMessage(ServerMessage):
    entity_id: str
    state: LightState
