import asyncio
import json
import logging
import os
from asyncio import AbstractEventLoop
from typing import Callable, Optional

import websockets
from homeassistant.components.event_observer import EventObserver
from homeassistant.home_assistant_authenticator import auth
from homeassistant.model.ha_income_message import *
from loguru import logger
from mediator.components.base_component import BaseComponent
from mediator.components.cover.cover_component import Cover
from mediator.components.light.light_component import Light
from mediator.components.switch.switch_component import Switch
from mediator.components.weather_component import Weather
from websockets.client import WebSocketClientProtocol

from .home_assistant_state_helper import HomeAssistantStateRequestHelper
from .model.ha_outcome_message import HaOutcomeMessage


class HomeAssistantClient:
    state_request_helper = HomeAssistantStateRequestHelper()
    HOME_ASSISTANT_URL = os.getenv("HASS_WS_ADDRESS")
    websocket: Optional[WebSocketClientProtocol] = None
    MESSAGE_TYPE = "type"
    event_observer: EventObserver
    callback_message: Callable[[BaseComponent], None]

    def __init__(self, loop: AbstractEventLoop, event_observer: EventObserver):
        self.event_observer = event_observer
        loop.create_task(self.start_haws_client())

    async def start_haws_client(self):
        logger.info(f"Starting HomeAssistant client websocket ....")
        logger.info(f"Websocket address: {self.HOME_ASSISTANT_URL}")
        await self.connect()

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.HOME_ASSISTANT_URL)
        except Exception as e:
            logger.error(f"Error connecting to HomeAssistant: {e}")
            await self.start_reconnection()
            return

        logger.info(f"Conencted to HomeAssistant!")

        response = await self.websocket.recv()
        result = await auth(self.websocket)
        if result == False:
            return
        await self.handle_message(response)
        await self.event_observer.subscribe_to_state(self.websocket)
        await self.listen_for_message()

    async def listen_for_message(self):
        try:
            while True:
                response = await self.websocket.recv()
                await self.handle_message(response)
        except Exception as e:
            self.websocket = None
            logger.error(f"Connection lost!:\n{e}")
            await self.start_reconnection()

    async def start_reconnection(self):
        await asyncio.sleep(10)
        logger.info("Start reconnection")
        await self.connect()

    def send_data(self, data: HaOutcomeMessage):
        self.state_request_helper.save_if_state_requested(data)
        json_message = json.dumps(data.model_dump(exclude_none=True))
        asyncio.create_task(self.send(json_message))

    async def send(self, message):
        try:
            if self.websocket:
                await self.websocket.send(message)
            else:
                logger.warning(f"websocket not initialized!")
        except Exception as e:
            logger.error(f"Send message error!\n {e}")

    async def handle_message(self, message):
        try:
            ha_message = HaIncomeMessage.model_validate_json(message, strict=False)
            if ha_message.type == "event" and ha_message.event:
                await self.process_state_changed(ha_message.event)
            elif self.state_request_helper.is_state_request_message(ha_message):
                await self.state_request_helper.process_message(
                    ha_message, self.process_state_changed
                )
        except Exception as e:
            logger.error(f"Error parsing message: {message}")
            logger.error(e)

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
        elif domain == "weather" and self.callback_message:
            weather = Weather(state)
            self.callback_message(weather)

    def set_message_callback(self, callback: Callable[[BaseComponent], None]):
        self.callback_message = callback
