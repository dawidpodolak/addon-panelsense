import asyncio
import json
from asyncio import AbstractEventLoop
from http import HTTPStatus
from typing import Callable, Optional

import websockets
from loging.logger import _LOGGER
from mediator.components.base_component import BaseComponent
from mediator.components.cover.cover_component import Cover
from mediator.components.light.light_component import Light
from pydantic import ValidationError
from server.client.client_authenticator import ClientAuthenticator
from server.model.base import ServerOutgoingMessage
from server.model.cover import CoverMessage
from server.model.error import ErrorCode, ErrorResponse
from server.model.light import *
from server.model.light import ServerMessage
from server.model.server_credentials import ServerCredentials
from websockets.client import WebSocketClientProtocol
from websockets.http11 import Request, Response
from websockets.server import ServerConnection


class PanelSenseServer:
    client_authenticator: ClientAuthenticator

    SENSE_SERVER_PORT = 8652

    websocket_server: WebSocketClientProtocol

    connected_clients = set()
    callback = None

    def __init__(self, loop: AbstractEventLoop, server_credentials: ServerCredentials):
        loop.create_task(self.start_sense_server())
        self.client_authenticator = ClientAuthenticator(server_credentials)

    async def message_handler(self, websocket: WebSocketClientProtocol):
        auth_message = await websocket.recv()

        sense_client = await self.client_authenticator.authenticate(
            auth_message, websocket
        )

        if not sense_client:
            _LOGGER.info(f"Client not authenticated! Close connection.")
            await websocket.close()
            return

        self.connected_clients.add(sense_client)

        try:
            async for message in websocket:
                self.handle_message(websocket, message)
                print(f"Reveived message:\n {message}")
        except websockets.exceptions.ConnectionClosedError as e:
            _LOGGER.error(f"Client disconnected! {e}")
        finally:
            self.connected_clients.remove(sense_client)
            _LOGGER.info(f"Client disconnected! {sense_client.name}")

    async def process_request(
        self, function: Callable[[ServerConnection, Request], Optional[Response]]
    ):
        print(f"Connection request!")
        pass

    async def start_sense_server(self):
        print(f"Server starting at ws://localhost:{self.SENSE_SERVER_PORT}")
        self.websocket_server = await websockets.serve(
            self.message_handler, "0.0.0.0", self.SENSE_SERVER_PORT
        )
        await self.websocket_server.serve_forever()

    async def send_message_async(self, message: BaseComponent):
        _LOGGER.info(f"Connected clients: {len(self.connected_clients)}")
        for client in self.connected_clients:
            print(f"SERVER ->: {message.get_message_for_client()}\n")
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

    def handle_message(self, client: WebSocketClientProtocol, message):
        try:
            client_message = ClientIncomingMessage.model_validate_json(message)
            self.process_client_message_ha_action(client, client_message.type, message)
            _LOGGER.debug(f"CLIENT -> handle_message type: {client_message}")
        except ValidationError as e:
            print(f"SERVER ERROR -> {message}")
            self.send_error(client, ErrorCode.INVALID_DATA, "Invalid data")
            return

    def process_client_message_ha_action(
        self, client: WebSocketClientProtocol, type: MessageType, message
    ):
        if type == MessageType.HA_ACTION_LIGHT:
            light_incoming_message = LightIncomingMessage.model_validate_json(message)
            light = Light(None, light_incoming_message=light_incoming_message)
            self.callback(light)
            _LOGGER.debug(
                f"CLIENT -> process_client_message_ha_action: {light_incoming_message}"
            )

    def set_message_callback(self, callback):
        self.callback = callback

    def handle_light(self, client: WebSocketClientProtocol, message):
        light_message: LightMessage
        try:
            light_message = LightMessage.model_validate_json(message)
        except ValidationError as e:
            print(f"SERVER ERROR -> {message}")
            self.send_error(client, ErrorCode.INVALID_DATA, "Invalid light data")
            return

    def handle_cover(self, client: WebSocketClientProtocol, message):
        cover_message: CoverMessage
        try:
            cover_message = CoverMessage.model_validate_json(message)
        except ValidationError as e:
            print(f"SERVER ERROR -> {message}")
            self.send_error(client, ErrorCode.INVALID_DATA, "Invalid cover data")
            return

        cover = Cover(cover_message=cover_message)
        self.callback(cover)
