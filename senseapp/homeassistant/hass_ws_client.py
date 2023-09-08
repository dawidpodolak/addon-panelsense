import json
import websockets
import logging
import asyncio
from homeassistant.auth_ha import auth
from homeassistant.components.event_observer import EventObserver
from asyncio import AbstractEventLoop
from homeassistant.model.ha_message import *


class HomeAssistantClient:

    HOME_ASSISTANT_URL = "ws://172.30.32.1:8123/api/websocket"
    websocket = None
    MESSAGE_TYPE = "type"
    event_observer: EventObserver

    def __init__(self, loop: AbstractEventLoop, event_observer: EventObserver):
        self.event_observer = event_observer
        loop.create_task(self.start_haws_client())

    async def start_haws_client(self):
        global websocket
        logging.basicConfig(
            format="%(message)s",
            level=logging.DEBUG,
        )
        print(f"Starting websocket ....")
        websocket = await websockets.connect(self.HOME_ASSISTANT_URL)
        print(f"Websocket started!")

        response = await websocket.recv()
        await self.handle_message(response)
        print(f"response1: {response}")
        await self.event_observer.subscribe_to_state(websocket)
        await self.listen_for_message()

    async def listen_for_message(self):
        while True:
            response = await websocket.recv()
            await self.handle_message(response)

    async def send_data(self, data):
        global websocket
        if websocket:
            await websocket.send(data)
        else:
            print(f"websocket not initialized!")

    async def handle_message(self, message):
        jsonData = json.loads(message)

        messageType = jsonData.get(self.MESSAGE_TYPE)
        ha_message = HaMessage.model_validate_json(message)
        if ha_message.type == "auth_required":
            await auth(websocket, message)
        elif ha_message.type == "event" and ha_message.event:
            await self.event_observer.handle_state(ha_message.event)

    def set_message_callback(self, callback):
        self.event_observer.set_message_callback(callback)
