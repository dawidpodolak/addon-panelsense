import json
from homeassistant.model.ha_message import HaEvent
from homeassistant.ids import get_message_id
from .light import process_light_state


class EventObserver:
    STATE_SUBSCRIPTION = {
        "id": get_message_id(),
        "type": "subscribe_events",
        "event_type": "state_changed"
    }

    async def subscribe_to_state(self, websocket):
        await websocket.send(json.dumps(self.STATE_SUBSCRIPTION))

    async def handle_state(self, event: HaEvent):
        entity = event.data.entity_id
        state = event.data.new_state.state
        await self.process_state(entity, state)

    async def process_state(self, entity, state):
        domain = entity.split('.')[0]
        print(f"domain: {domain}")
        if domain == 'light':
            await process_light_state(entity, state)
