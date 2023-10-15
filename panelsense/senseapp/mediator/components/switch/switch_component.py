from typing import Optional

from homeassistant.ids import get_message_id
from homeassistant.model.ha_income_message import HaEventData, SwitchAttributes
from homeassistant.model.ha_outcome_message import *
from mediator.components.base_component import BaseComponent
from server.model.switch import *


class Switch(BaseComponent):
    on: bool = False
    friendly_name: Optional[str] = None
    icon: Optional[str] = None

    def __init__(
        self,
        haEventData: Optional[HaEventData] = None,
        switch_message: Optional[SwitchIncomingMessage] = None,
    ):
        if haEventData:
            self.updateState(haEventData)
        elif switch_message:
            self.update_state_from_server(switch_message.data)

    def updateState(self, haEventData: HaEventData):
        attributes = SwitchAttributes(**haEventData.new_state.attributes)
        self.entity_id = haEventData.entity_id
        self.on = haEventData.new_state.state == "on"
        self.friendly_name = attributes.friendly_name
        self.icon = attributes.icon

    def update_state_from_server(
        self, light_incoming_message: SwitchIncomingDataMessage
    ):
        self.entity_id = light_incoming_message.entity_id
        self.on = light_incoming_message.on

    def get_message_for_home_assistant(self) -> HaOutcomeMessage:
        return HaCallServiceMessage(
            id=get_message_id(),
            domain="switch",
            service=self.get_ha_service(),
            target=Target(entity_id=self.entity_id),
        )

    def get_ha_service(self) -> str:
        if self.on:
            return "turn_on"
        else:
            return "turn_off"

    def get_message_for_client(self) -> SwitchOutcomingMessage:
        data = SwitchOutcomingDataMessage(
            entity_id=self.entity_id,
            on=self.on,
            friendly_name=self.friendly_name,
            icon=self.icon,
        )
        return SwitchOutcomingMessage(data=data)
