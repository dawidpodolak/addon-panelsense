import asyncio
import json
import logging
from asyncio import AbstractEventLoop

import websockets
from homeassistant.components.event_observer import EventObserver
from homeassistant.home_assistant_authenticator import auth
from homeassistant.model.ha_income_message import *
from loging.logger import _LOGGER
from mediator.components.cover.cover_component import Cover
from mediator.components.light.light_component import Light


class HomeAssistantClient:
    HOME_ASSISTANT_URL = "ws://172.30.32.1:8123/api/websocket"
    websocket = None
    MESSAGE_TYPE = "type"
    event_observer: EventObserver
    callback_message = None

    def __init__(self, loop: AbstractEventLoop, event_observer: EventObserver):
        self.event_observer = event_observer
        loop.create_task(self.start_haws_client())

    async def start_haws_client(self):
        global websocket
        # logging.basicConfig(
        #     format="%(message)s",
        #     level=logging.DEBUG,
        # )
        _LOGGER.info(f"Starting HomeAssistant client websocket ....")
        websocket = await websockets.connect(self.HOME_ASSISTANT_URL)
        _LOGGER.info(f"HomeAssistant websockent client started!")

        response = await websocket.recv()
        await self.handle_message(response)
        await self.event_observer.subscribe_to_state(websocket)
        await self.listen_for_message()

    async def listen_for_message(self):
        while True:
            response = await websocket.recv()
            await self.handle_message(response)

    def send_data(self, data):
        global websocket
        json_message = json.dumps(data.model_dump(exclude_none=True))
        _LOGGER.info(f"-> HA: {json_message}\n")
        if websocket:
            asyncio.create_task(websocket.send(json_message))
        else:
            _LOGGER.info(f"websocket not initialized!")

    async def handle_message(self, message):
        _LOGGER.info(f"HA ->: {message}\n")
        ha_message = HaIncomeMessage.model_validate_json(message)
        if ha_message.type == "auth_required":
            await auth(websocket, message)
        elif ha_message.type == "event" and ha_message.event:
            await self.process_state_changed(ha_message.event)

    async def process_state_changed(self, event: HaEvent):
        entity = event.data.entity_id
        state: HaEventData = event.data
        domain = entity.split(".")[0]
        if domain == "light" and self.callback_message:
            light = Light(state)
            self.callback_message(light)
        elif domain == "cover" and self.callback_message:
            cover = Cover(state)
            self.callback_message(cover)

    def set_message_callback(self, callback):
        self.callback_message = callback
