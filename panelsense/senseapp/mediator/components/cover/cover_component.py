from typing import Optional

from homeassistant.ids import get_message_id
from homeassistant.model.ha_income_message import CoverAttributes, HaEventData
from homeassistant.model.ha_outcome_message import *
from loging.logger import _LOGGER
from mediator.components.base_component import BaseComponent
from server.model.cover import *


class Cover(BaseComponent):
    entity_id: str
    state: Optional[str] = None
    friendly_name: Optional[str] = None
    device_class: Optional[str] = None
    position: Optional[int] = None
    tils_position: Optional[int] = None
    supported_features: Optional[int] = None

    def __init__(
        self,
        haEventData: Optional[HaEventData] = None,
        cover_message: Optional[CoverIncomingMessage] = None,
    ):
        if haEventData:
            self.update_state_from_ha(haEventData)
        elif cover_message:
            self.update_state_from_server(cover_message.data)

    def update_state_from_ha(self, haEventData: HaEventData):
        attributes = CoverAttributes(**haEventData.new_state.attributes)
        self.entity_id = haEventData.entity_id
        self.position = attributes.current_position
        self.friendly_name = attributes.friendly_name
        self.device_class = attributes.device_class
        self.tils_position = attributes.current_tilt_position
        self.state = haEventData.new_state.state
        self.supported_features = attributes.supported_features

    def update_state_from_server(self, cover_message: CoverIncomingDataMessage):
        self.entity_id = cover_message.entity_id
        self.position = cover_message.position
        self.state = cover_message.state

    def get_message_for_home_assistant(self) -> HaOutcomeMessage:
        call_service = HaCallServiceMessage(
            id=get_message_id(),
            domain="cover",
            service=self.get_cover_service_data(),
            service_data=CoverServiceData(position=self.position),
            target=Target(entity_id=self.entity_id),
        )
        print(f"Set posistion -----> {self.position} --> {call_service.service_data}")
        print(
            f"model is -----> {call_service.service_data} --> {call_service.model_dump_json(exclude_none=True)}"
        )
        return call_service

    def get_message_for_client(self) -> CoverOutcomingMessage:
        data = CoverOutcomingDataMessage(
            entity_id=self.entity_id,
            state=self.state,
            position=self.position,
            tilt_position=self.tils_position,
            friendly_name=self.friendly_name,
            device_class=self.device_class,
            supported_features=self.supported_features,
        )
        return CoverOutcomingMessage(type=MessageType.HA_ACTION_COVER, data=data)

    def get_cover_service_data(self) -> str:
        if self.state == "close":
            return "close_cover"
        elif self.state == "open":
            return "open_cover"
        elif self.state == "stop":
            return "stop_cover"
        elif self.position:
            return "set_cover_position"
        else:
            return "open_cover"
