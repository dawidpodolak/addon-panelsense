from pydantic import BaseModel
from enum import Enum


class ErrorCode(Enum):
    MISSING_ENTITY_ID = "MISSING_ENTITY_ID"
    INVALID_DATA = "INVALID_DATA"


class Error(BaseModel):
    error_code: ErrorCode
    message: str
