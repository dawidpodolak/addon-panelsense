import json
from homeassistant.model.ha_income_message import HaEvent, HaEventData, HaEventState
from homeassistant.ids import get_message_id


class EventObserver:
    STATE_SUBSCRIPTION = {
        "id": get_message_id(),
        "type": "subscribe_events",
        "event_type": "state_changed"
    }

    callback_message = None

    async def subscribe_to_state(self, websocket):
        await websocket.send(json.dumps(self.STATE_SUBSCRIPTION))

    async def handle_state(self, event: HaEvent):
        entity = event.data.entity_id
        state = event.data
        await self.process_state(entity, state)

    async def process_state(self, entity, state: HaEventData):
        domain = entity.split('.')[0]
        if domain == 'light' and self.callback_message:
            self.callback_message(state)

    def set_message_callback(self, callback):
        self.callback_message = callback
