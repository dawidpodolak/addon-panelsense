import asyncio
import json
import os

from loging.logger import _LOGGER
from pydantic import BaseModel
from websockets import WebSocketClientProtocol

HOME_ASSISTANT_TOKEN = os.getenv('SUPERVISOR_TOKEN')

class HASupervisor(BaseModel):
    type: str = "auth"
    access_token: str

async def auth(websocket, message):

    _LOGGER.info(f"Supervisor token: {HOME_ASSISTANT_TOKEN}")
    auth_message = HASupervisor(access_token = HOME_ASSISTANT_TOKEN)
    await websocket.send(auth_message.model_dump_json())
