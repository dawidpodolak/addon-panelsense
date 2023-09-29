from enum import Enum

from pydantic import BaseModel

from .base import ClientIncomingMessage, MessageType, ServerOutgoingMessage


class AuthenticationIncomingMessage(ClientIncomingMessage):
    type: MessageType
    token: str
    name: str
    version_code: int
    version_name: str


class AuthResult(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class AuthenticationRespone(ServerOutgoingMessage):
    auth_result: AuthResult
    type: MessageType = MessageType.AUTH
