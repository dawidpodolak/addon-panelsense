from enum import Enum

from pydantic import BaseModel


class MessageType(Enum):
    AUTH = "auth"
    ERROR = "error"
    HA_ACTION_LIGHT = "ha_action_light"
    HA_ACTION_COVER = "ha_action_cover"


# extended class should implement type: MessageType
class ClientIncomingMessage(BaseModel):
    type: MessageType


# extended class should implement type: MessageType


class ServerOutgoingMessage(BaseModel):
    pass
