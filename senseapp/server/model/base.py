from enum import Enum

from pydantic import BaseModel


class MessageType(Enum):
    AUTH = "auth"
    ERROR = "error"

# extended class should implement type: MessageType


class ClientIncomingMessage(BaseModel):
    pass

# extended class should implement type: MessageType


class ServerOutgoingMessage(BaseModel):
    pass
