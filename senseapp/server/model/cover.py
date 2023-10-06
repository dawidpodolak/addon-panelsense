from typing import List, Optional

from pydantic import BaseModel
from server.model.light import ServerMessage

from .base import *


class CoverState(BaseModel):
    state: Optional[str] = None
    position: Optional[int] = None


class CoverMessage(ServerMessage):
    entity_id: str
    state: Optional[str] = None
    position: Optional[int] = None


# Incoming messages - received from client
class CoverIncomingDataMessage(BaseModel):
    entity_id: str
    state: Optional[str] = None
    position: Optional[int] = None


class CoverIncomingMessage(ClientIncomingMessage):
    type: MessageType = MessageType.HA_ACTION_COVER
    data: CoverIncomingDataMessage


# Outcoming message - sends from server to client
class CoverOutcomingDataMessage(BaseModel):
    entity_id: str
    state: Optional[str] = None
    position: Optional[int] = None
    tilt_position: Optional[int] = None


class CoverOutcomingMessage(ServerOutgoingMessage):
    type: MessageType = MessageType.HA_ACTION_COVER
    data: CoverOutcomingDataMessage
