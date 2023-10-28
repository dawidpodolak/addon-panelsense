from typing import Callable

from loguru import logger

from .model.ha_income_message import HaEvent, HaEventState, HaEventData, HaIncomeMessage
from .model.ha_outcome_message import HaOutcomeMessage


class HomeAssistantStateRequestHelper():
    reqest_message_id: int = -1

    def save_if_state_requested(self, message: HaOutcomeMessage):
        if message.type == "get_states" and message.id != None:
            self.reqest_message_id = message.id

    def is_state_request_message(self, incoming_message: HaIncomeMessage) -> bool:
        is_state_request_message = self.reqest_message_id == incoming_message.id

        return is_state_request_message

    async def process_message(self, message: HaIncomeMessage, callback):
        result_array = message.result
        if result_array == None:
            return

        for result in result_array:
            state = HaEventState(
                entity_id = result.entity_id,
                state=result.state,
                attributes=result.attributes
            )
            ha_event_data = HaEventData(
                entity_id=result.entity_id,
                new_state=state
            )
            ha_event = HaEvent(
                event_type= "event",
                data = ha_event_data
            )

            await callback(ha_event)

        self.reqest_message_id = -1