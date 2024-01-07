from typing import Optional

from homeassistant.model.ha_income_message import (HaEventData, HaEventState,
                                                   SensorAttributes)
from homeassistant.model.ha_outcome_message import *
from server.model.base import MessageType, ServerOutgoingMessage
from server.model.sensor import (SensorOutcomingDataMessage,
                                 SensorOutcomingMessage)

from .base_component import BaseComponent


class Sensor(BaseComponent):
    entity: str
    state: str
    attributes: SensorAttributes

    def __init__(self, ha_event_data: HaEventData):
        self.entity = ha_event_data.entity_id
        self.state = ha_event_data.new_state.state
        self.attributes = SensorAttributes(**ha_event_data.new_state.attributes)

    def get_message_for_client(self) -> ServerOutgoingMessage:
        return SensorOutcomingMessage(
            type=self.get_message_type(), data=self.get_data()
        )

    def get_message_type(self) -> MessageType:
        if self.entity.startswith("binary_sensor"):
            return MessageType.HA_ACTION_BINARY_SENSOR
        else:
            return MessageType.HA_ACTION_SENSOR

    def get_data(self) -> SensorOutcomingDataMessage:
        return SensorOutcomingDataMessage(
            entity_id=self.entity,
            state=self.state,
            state_class=self.attributes.state_class,
            battery_level=self.attributes.battery_level,
            unit_of_measurement=self.attributes.unit_of_measurement,
            icon=self.attributes.icon,
            device_class=self.attributes.device_class,
            friendly_name=self.attributes.friendly_name,
        )
