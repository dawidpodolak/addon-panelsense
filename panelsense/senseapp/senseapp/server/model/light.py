from typing import List, Optional

from pydantic import BaseModel

from .base import *


class ServerMessage(BaseModel):
    entity_id: str


class LightState(BaseModel):
    on: bool = False
    brightness: int = 0
    color_mode: Optional[str] = None
    rgb_color: Optional[List[int]] = None
    color_temp_kelvin: Optional[int] = None


# Incoming messages - received from client
class LightIncomingDataMessage(BaseModel):
    entity_id: str
    on: bool = False
    brightness: Optional[int] = None
    color_mode: Optional[str] = None
    rgb_color: Optional[List[int]] = None
    color_temp_kelvin: Optional[int] = None
    max_color_temp_kelvin: Optional[int] = None
    min_color_temp_kelvin: Optional[int] = None
    color_temp_kelvin: Optional[int] = None
    supported_color_modes: Optional[List[str]] = None


class LightIncomingMessage(ClientIncomingMessage):
    type: MessageType = MessageType.HA_ACTION_LIGHT
    data: LightIncomingDataMessage


# Outcoming message - sends from server to client
class LightOutcomingDataMessage(BaseModel):
    entity_id: str
    on: bool = False
    brightness: Optional[int] = None
    color_mode: Optional[str] = None
    rgb_color: Optional[List[int]] = None
    color_temp_kelvin: Optional[int] = None
    max_color_temp_kelvin: Optional[int] = None
    min_color_temp_kelvin: Optional[int] = None
    color_temp_kelvin: Optional[int] = None
    supported_color_modes: Optional[List[str]] = None
    friendly_name: Optional[str] = None
    icon: Optional[str] = None


class LightOutcomingMessage(ServerOutgoingMessage):
    type: MessageType = MessageType.HA_ACTION_LIGHT
    data: LightOutcomingDataMessage
