from enum import Enum

from .base import MessageType, ServerOutgoingMessage


class ErrorCode(Enum):
    MISSING_ENTITY_ID = "MISSING_ENTITY_ID"
    INVALID_DATA = "INVALID_DATA"


class ErrorResponse(ServerOutgoingMessage):
    error_code: ErrorCode
    message: str
    type: MessageType = MessageType.ERROR
