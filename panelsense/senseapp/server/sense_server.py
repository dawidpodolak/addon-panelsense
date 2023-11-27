import asyncio
import json
from asyncio import AbstractEventLoop
from http import HTTPStatus
from typing import Callable, Optional, Set

import websockets
from loguru import logger
from mediator.components.base_component import BaseComponent
from mediator.components.cover.cover_component import Cover
from mediator.components.light.light_component import Light
from mediator.components.state_request_component import StateRequest
from mediator.components.switch.switch_component import Switch
from pydantic import ValidationError
from server.client.client_authenticator import ClientAuthenticator
from server.client.sense_client import SenseClient
from server.database.sense_database import SenseDatabase
from server.model.cover import *
from server.model.error import ErrorCode, ErrorResponse
from server.model.light import *
from server.model.server_credentials import ServerCredentials
from server.model.switch import *
from websockets.client import WebSocketClientProtocol
from websockets.exceptions import ConnectionClosedError
from websockets.http11 import Request, Response
from websockets.server import ServerConnection

from .client_connection_helper import ClientConectionHelper


class PanelSenseServer(ClientConectionHelper):
    client_authenticator: ClientAuthenticator

    SENSE_SERVER_PORT = 8652

    websocket_server: WebSocketClientProtocol
    loop: AbstractEventLoop
    callback: Callable[[BaseComponent], None]
    database: SenseDatabase

    def __init__(
        self,
        loop: AbstractEventLoop,
        server_credentials: ServerCredentials,
        database: SenseDatabase,
    ):
        self.database = database
        self.loop = loop
        loop.create_task(self.start_sense_server())
        self.connected_clients = database.get_sense_clients()
        self.client_authenticator = ClientAuthenticator(server_credentials, database)

    def get_client(self) -> Set[SenseClient]:
        return self.connected_clients

    async def message_handler(self, websocket: WebSocketClientProtocol):
        logger.info(f"Attempt to connect: {websocket.remote_address}")
        auth_message = await websocket.recv()

        sense_client = await self.client_authenticator.authenticate(
            auth_message, websocket, self.get_client
        )

        if not sense_client:
            logger.info(f"Client not authenticated! Close connection.")
            await websocket.close()
            return

        self.on_client_connected(sense_client)

        try:
            async for message in websocket:
                try:
                    self.handle_message(websocket, message)
                    logger.debug(f"Received message:\n {message}")
                except Exception as e:
                    logger.debug(f"Error in hande_message!")
                    logger.error(e)
        except websockets.exceptions.ConnectionClosedError as e:
            sense_client.websocket = None
            sense_client.is_online = False
            logger.error(f"Client disconnected! {e}")
        except Exception as e:
            logger.error(e)
        finally:
            logger.info(f"Client disconnected! {sense_client.details.name}")
            self.on_client_disconnected(sense_client)

    async def start_sense_server(self):
        logger.info(f"Server starting at ws://localhost:{self.SENSE_SERVER_PORT}")
        self.websocket_server = await websockets.serve(
            self.message_handler, "0.0.0.0", self.SENSE_SERVER_PORT
        )
        await self.websocket_server.serve_forever()

    async def send_message_async(self, message: BaseComponent):
        for client in self.connected_clients:
            # logger.info(f"SERVER ->: {message.get_message_for_client()}\n")
            await client.send(
                message.get_message_for_client().model_dump_json(exclude_none=True)
            )

    async def send_error_async(
        self, client: WebSocketClientProtocol, error: ErrorResponse
    ):
        await client.send(error.model_dump_json(exclude_none=True))

    def send_message(self, component: BaseComponent):
        asyncio.create_task(self.send_message_async(component))

    def send_error(
        self, client: WebSocketClientProtocol, error_code: ErrorCode, error_message: str
    ):
        asyncio.create_task(
            self.send_error_async(
                client, ErrorResponse(error_code=error_code, message=error_message)
            )
        )

    def update_sense_client_config(self, installation_id: str, config: str):
        sense_client: Optional[SenseClient] = None

        for sc in self.connected_clients:
            if sc.details.installation_id == installation_id:
                sense_client = sc

        logger.info(
            f"Updadate sense client {installation_id} with config: {sense_client == None}"
        )
        if sense_client:
            sense_client.configuration_str = config
            self.database.update_sense_client_configuration(installation_id, config)
            sense_client.prepare_config()
            asyncio.run(sense_client.send_config())

    def handle_message(self, client: WebSocketClientProtocol, message):
        try:
            client_message = ClientIncomingMessage.model_validate_json(message)
            self.process_client_message_ha_action(client, client_message.type, message)
            # logger.debug(f"CLIENT -> handle_message type: {client_message}")
        except ValidationError as e:
            logger.error(f"SERVER ERROR -> {message}")
            self.send_error(client, ErrorCode.INVALID_DATA, "Invalid data")
            return

    def process_client_message_ha_action(
        self, client: WebSocketClientProtocol, type: MessageType, message
    ):
        if type == MessageType.HA_ACTION_LIGHT:
            light_incoming_message = LightIncomingMessage.model_validate_json(message)
            light = Light(None, light_incoming_message=light_incoming_message)
            self.callback(light)
        elif type == MessageType.HA_ACTION_COVER:
            cover_incoming_message = CoverIncomingMessage.model_validate_json(message)
            cover = Cover(None, cover_message=cover_incoming_message)
            self.callback(cover)
        elif type == MessageType.HA_ACTION_SWITCH:
            switch_incoming_message = SwitchIncomingMessage.model_validate_json(message)
            switch = Switch(switch_message=switch_incoming_message)
            self.callback(switch)
        elif type == MessageType.HA_STATE_REQUEST:
            state_request = StateRequest()
            self.callback(state_request)

    def set_message_callback(self, callback: Callable[[BaseComponent], None]):
        self.callback = callback
