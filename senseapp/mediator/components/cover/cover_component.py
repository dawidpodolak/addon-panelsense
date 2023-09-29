from typing import Optional

from homeassistant.ids import get_message_id
from homeassistant.model.ha_income_message import HaEventData
from homeassistant.model.ha_outcome_message import *
from mediator.components.base_component import BaseComponent
from mediator.components.cover.cover_model import CoverModel
from mediator.components.cover.cover_state import CoverState, State
from server.model.cover import CoverMessage


class Cover(BaseComponent):

    cover_state = CoverState()

    def __init__(self, haEventData: Optional[HaEventData] = None, cover_message: Optional[CoverMessage] = None):
        if haEventData:
            self.update_state_from_ha(haEventData)
        elif cover_message:
            self.update_state_from_server(cover_message)

    def update_state_from_ha(self, haEventData: HaEventData):
        self.entity_id = haEventData.entity_id
        self.cover_state.current_position = haEventData.new_state.attributes.current_position
        self.cover_state.state = self.parse_state(haEventData.new_state.state)

    def update_state_from_server(self, cover_message: CoverMessage):
        self.entity_id = cover_message.entity_id
        self.cover_state.current_position = cover_message.position
        self.cover_state.state = self.parse_state(cover_message.state)

    def parse_state(self, state: str) -> Optional[State]:
        if state:
            try:
                return State(state)
            except ValueError:
                return State.OPEN
        else:
            return None

    def getHomeAssistantMessage(self) -> HaOutcomeMessage:
        return HaCallServiceMessage(
            id=get_message_id(),
            domain='cover',
            service=self.get_cover_service_data(),
            # TODO change to cover service data
            service_data=LightServiceData(
                position=self.cover_state.current_position
            ),
            target=Target(entity_id=self.entity_id),
        )

    def getSenseServerMessage(self):
        return CoverModel(
            entity_id=self.entity_id,
            state=self.cover_state.state.value,
            position=self.cover_state.current_position
        )

    def get_cover_service_data(self) -> str:
        state = self.cover_state.state
        position = self.cover_state.current_position
        if state == State.CLOSED:
            return 'close_cover'
        elif state == State.OPEN:
            return 'open_cover'
        elif state == State.STOP:
            return 'stop_cover'
        elif position:
            return 'set_cover_position'
        else:
            return 'open_cover'
