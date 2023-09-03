from pydantic import BaseModel
from typing import Optional


class HaEventState(BaseModel):
    entity_id: str
    state: str


class HaEventData(BaseModel):
    entity_id: str
    new_state: HaEventState


class HaEvent(BaseModel):
    event_type: str
    data: HaEventData


class HaMessage(BaseModel):
    id: Optional[int] = None
    type: str
    event: Optional[HaEvent] = None
