import asyncio
import json
import os
from typing import Optional

from loging.logger import _LOGGER
from pydantic import BaseModel
from websockets import WebSocketClientProtocol

HOME_ASSISTANT_TOKEN = os.getenv('SUPERVISOR_TOKEN')

class AuthMessage(BaseModel):
    type: str = "auth"
    access_token: str

class AuthRespone(BaseModel):
    type:str
    ha_version: Optional[str] = None
    message: Optional[str] = None

async def auth(websocket) -> bool:
    auth_message = AuthMessage(access_token = HOME_ASSISTANT_TOKEN)
    await websocket.send(auth_message.model_dump_json())
    auth_response_json= await websocket.recv()
    auth_response = AuthRespone.model_validate_json(auth_response_json)
    if auth_response.type == "auth_ok":
        return True
    else:
        _LOGGER.warn(f"Authentication error. {auth_response.message}")
        return False

