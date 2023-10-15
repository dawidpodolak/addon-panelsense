from typing import Optional

from pydantic import BaseModel
from server.model.light import ServerMessage

from .base import *


# Incoming messages - received from client
class SwitchIncomingDataMessage(BaseModel):
    entity_id: str
    on: bool = False


class SwitchIncomingMessage(ClientIncomingMessage):
    type: MessageType = MessageType.HA_ACTION_SWITCH
    data: SwitchIncomingDataMessage


# Outcoming message - sends from server to client
class SwitchOutcomingDataMessage(BaseModel):
    entity_id: str
    on: bool = False
    icon: Optional[str] = None
    friendly_name: Optional[str] = None


class SwitchOutcomingMessage(ServerOutgoingMessage):
    type: MessageType = MessageType.HA_ACTION_SWITCH
    data: SwitchOutcomingDataMessage
