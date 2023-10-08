from enum import Enum

from pydantic import BaseModel

from .base import ClientIncomingMessage, MessageType, ServerOutgoingMessage


class AuthData(BaseModel):
    token: str
    name: str
    version_code: int
    version_name: str
    installation_id: str


class AuthenticationIncomingMessage(ClientIncomingMessage):
    type: MessageType
    data: AuthData


class AuthResult(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class AuthResponseData(BaseModel):
    auth_result: AuthResult


class AuthenticationRespone(ServerOutgoingMessage):
    data: AuthResponseData
    type: MessageType = MessageType.AUTH
