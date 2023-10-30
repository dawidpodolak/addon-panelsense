from enum import Enum

from pydantic import BaseModel


class MessageType(Enum):
    AUTH = "auth"
    ERROR = "error"
    CONFIGURATION = "configuration"
    HA_ACTION_COVER = "ha_action_cover"
    HA_ACTION_LIGHT = "ha_action_light"
    HA_ACTION_SWITCH = "ha_action_switch"
    HA_STATE_REQUEST = "ha_state_request"
    HA_ACTION_WEATHER = "ha_action_weather"


# extended class should implement type: MessageType
class ClientIncomingMessage(BaseModel):
    type: MessageType


# extended class should implement type: MessageType


class ServerOutgoingMessage(BaseModel):
    pass
