from typing import List, Optional

from .base import *


class SensorOutcomingDataMessage(BaseModel):
    entity_id: str
    state: Optional[str] = None
    state_class: Optional[str] = None
    battery_level: Optional[int] = None
    unit_of_measurement: Optional[str] = None
    icon: Optional[str] = None
    device_class: Optional[str] = None
    friendly_name: Optional[str] = None


class SensorOutcomingMessage(ServerOutgoingMessage):
    type: MessageType = MessageType.HA_ACTION_SENSOR
    data: SensorOutcomingDataMessage
