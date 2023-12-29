import json

from homeassistant.ids import get_message_id
from homeassistant.model.ha_income_message import HaEvent, HaEventData, HaEventState


class EventObserver:
    STATE_SUBSCRIPTION = {
        "id": get_message_id(),
        "type": "subscribe_events",
        "event_type": "state_changed",
    }

    async def subscribe_to_state(self, websocket):
        await websocket.send(json.dumps(self.STATE_SUBSCRIPTION))

    def set_message_callback(self, callback):
        self.callback_message = callback
