import asyncio
import json
import logging
import os
from asyncio import AbstractEventLoop
from typing import Callable

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

from .home_assistant_state_helper import HomeAssistantStateRequestHelper
from .model.ha_outcome_message import HaOutcomeMessage


class HomeAssistantClient:
    state_request_helper = HomeAssistantStateRequestHelper()
    HOME_ASSISTANT_URL = os.getenv("HASS_WS_ADDRESS")
    websocket = None
    MESSAGE_TYPE = "type"
    event_observer: EventObserver
    callback_message: Callable[[BaseComponent], None]

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
            # logger.debug(f"HA Message ->> {response}")
            await self.handle_message(response)

    def send_data(self, data: HaOutcomeMessage):
        global websocket
        self.state_request_helper.save_if_state_requested(data)
        json_message = json.dumps(data.model_dump(exclude_none=True))
        logger.info(f"-> HA: {json_message}\n")
        if websocket:
            asyncio.create_task(websocket.send(json_message))
        else:
            logger.info(f"websocket not initialized!")

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
