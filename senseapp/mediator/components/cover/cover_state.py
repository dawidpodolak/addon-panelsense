from enum import Enum
from typing import Optional

from pydantic import BaseModel


class State(Enum):
    CLOSED = "closed"
    OPEN = "open"
    OPENING = "opening"
    CLOSING = "closing"
    STOP = "stop"


class CoverState(BaseModel):
    state: Optional[State] = None
    supported_features: Optional[int] = None
    friendly_name: Optional[str] = None
    current_position: Optional[int] = None
