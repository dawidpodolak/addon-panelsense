import asyncio
import json
from homeassistant.ids import get_message_id

STATE_SUBSCRIPTION = {
    "id": get_message_id(),
    "type": "subscribe_events",
    "event_type": "state_changed"
}


async def subscribe_to_state(websocket):
    await websocket.send(json.dumps(STATE_SUBSCRIPTION))
