import asyncio
import json

from websockets import WebSocketClientProtocol

AUTH_REQUIRED = "auth_required"
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI3OTg2Y2NkZDQ2MDU0N2NiYjM2ZmQ1MTY5NDNkNTQ3OCIsImlhdCI6MTY5MzI0MDk0MCwiZXhwIjoyMDA4NjAwOTQwfQ.uTESAQpwckfE7YgvFc_8emK2Ge5XupFzRMBaUzvln8A"
AUTH_MESSAGE = {
    "type": "auth",
    "access_token": AUTH_TOKEN
}


async def auth(websocket, message):
    message_to_send = json.dumps(AUTH_MESSAGE)
    await websocket.send(message_to_send)
