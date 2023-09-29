from typing import List, Optional

from pydantic import BaseModel
from server.model.light import ServerMessage

from .base import ServerOutgoingMessage


class CoverState(BaseModel):
    state: Optional[str] = None
    position: Optional[int] = None


class CoverMessage(ServerMessage):
    entity_id: str
    state: Optional[str] = None
    position: Optional[int] = None
