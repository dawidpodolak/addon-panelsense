import asyncio
import json

STATE_SUBSCRIPTION = {
    "id": 18,
    "type": "subscribe_events",
    "event_type": "state_changed"
}


async def subscribe_to_state(websocket):
    await websocket.send(json.dumps(STATE_SUBSCRIPTION))
