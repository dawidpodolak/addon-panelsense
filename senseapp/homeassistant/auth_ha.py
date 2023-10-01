import asyncio
import json

from websockets import WebSocketClientProtocol

AUTH_REQUIRED = "auth_required"
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkMjU5OTM5N2NhNTU0ZjU3YWFmOWQ2NGNlMzFlYjQyZSIsImlhdCI6MTY5NjE3ODk4MiwiZXhwIjoyMDExNTM4OTgyfQ.n6p7E7lKyE2uKYZvnahTcNen_qhskkpsdOQvA9od_4I"
AUTH_MESSAGE = {"type": "auth", "access_token": AUTH_TOKEN}


async def auth(websocket, message):
    message_to_send = json.dumps(AUTH_MESSAGE)
    await websocket.send(message_to_send)
