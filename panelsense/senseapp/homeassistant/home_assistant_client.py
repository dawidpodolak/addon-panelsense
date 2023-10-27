import asyncio
import json
import logging
import os
from asyncio import AbstractEventLoop

import websockets
from homeassistant.components.event_observer import EventObserver
from homeassistant.home_assistant_authenticator import auth
from homeassistant.model.ha_income_message import *
from loguru import logger
from mediator.components.cover.cover_component import Cover
from mediator.components.light.light_component import Light
from mediator.components.switch.switch_component import Switch


class HomeAssistantClient:
    HOME_ASSISTANT_URL = os.getenv("HASS_WS_ADDRESS")
    websocket = None
    MESSAGE_TYPE = "type"
    event_observer: EventObserver
    callback_message = None

    def __init__(self, loop: AbstractEventLoop, event_observer: EventObserver):
        self.event_observer = event_observer
        loop.create_task(self.start_haws_client())

    async def start_haws_client(self):
        global websocket
        logger.info(f"Starting HomeAssistant client websocket ....")
        logger.info(f"Websocket address: {self.HOME_ASSISTANT_URL}")
        websocket = await websockets.connect(self.HOME_ASSISTANT_URL)
        logger.info(f"HomeAssistant websockent client started!")

        response = await websocket.recv()
        result = await auth(websocket)
        if result == False:
            return
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
        logger.info(f"-> HA: {json_message}\n")
        if websocket:
            asyncio.create_task(websocket.send(json_message))
        else:
            loguru.info(f"websocket not initialized!")

    async def handle_message(self, message):
        logger.info(f"HA ->: {message}\n")
        ha_message = HaIncomeMessage.model_validate_json(message, strict=False)
        if ha_message.type == "event" and ha_message.event:
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
        elif domain == "switch" and self.callback_message:
            switch = Switch(state)
            self.callback_message(switch)

    def set_message_callback(self, callback):
        self.callback_message = callback
