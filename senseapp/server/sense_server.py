import asyncio
import json
from asyncio import AbstractEventLoop
from http import HTTPStatus
from typing import Callable, Optional

import websockets
from mediator.components.base_component import BaseComponent
from mediator.components.cover.cover_component import Cover
from mediator.components.light.light_component import Light
from pydantic import ValidationError
from server.client.client_authenticator import ClientAuthenticator
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
        try:
            sense_client = await self.client_authenticator.authenticate(auth_message, websocket)
            print(f"auth_message: {auth_message}")
            self.connected_clients.add(websocket)
        except BaseException as e:
            await self.send_error_async(websocket, e)
            await websocket.close()
            return
        async for message in websocket:
            self.handle_message(websocket, message)
            print(f"Reveived message:\n {message}")

    async def process_request(self, function: Callable[[ServerConnection, Request], Optional[Response]]):

        print(f"Connection request!")
        pass

    async def process_request1(self, path, request_headers):
        authorization = request_headers["Authorization"]
        print(
            f"Connection request1!path: {path}, request_headers: {authorization}")
        if authorization is None:
            return HTTPStatus.UNAUTHORIZED, [], b"Missing token\n"

    async def start_sense_server(self):
        print(f"Server starting at ws://localhost:{self.SENSE_SERVER_PORT}")
        self.websocket_server = await websockets.serve(self.message_handler, "0.0.0.0", self.SENSE_SERVER_PORT)
        await self.websocket_server.serve_forever()

    async def send_message_async(self, message: BaseComponent):
        for client in self.connected_clients:
            print(f"SERVER ->: {message.getSenseServerMessage()}\n")
            await client.send(json.dumps(message.getSenseServerMessage().model_dump(exclude_none=True)))

    async def send_error_async(self, client: WebSocketClientProtocol, error: ErrorResponse):
        await client.send(error.model_dump_json(exclude_none=True))

    def send_message(self, component: BaseComponent):
        asyncio.create_task(self.send_message_async(component))

    def send_error(self, client: WebSocketClientProtocol, error_code: ErrorCode, error_message: str):
        asyncio.create_task(self.send_error_async(
            client, ErrorResponse(error_code=error_code, message=error_message)))

    def handle_message(self, client: WebSocketClientProtocol, message):
        server_message: ServerMessage
        try:
            server_message = ServerMessage.model_validate_json(message)
        except ValidationError as e:
            print(f"SERVER ERROR -> {message}")
            self.send_error(client, ErrorCode.MISSING_ENTITY_ID,
                            "Missing entity_id")
            return

        domain = server_message.entity_id.split('.')[0]
        if domain == 'light':
            self.handle_light(client, message)
        elif domain == 'cover':
            self.handle_cover(client, message)

    def set_message_callback(self, callback):
        self.callback = callback

    def handle_light(self, client: WebSocketClientProtocol, message):
        light_message: LightMessage
        try:
            light_message = LightMessage.model_validate_json(message)
        except ValidationError as e:
            print(f"SERVER ERROR -> {message}")
            self.send_error(client, ErrorCode.INVALID_DATA,
                            "Invalid light data")
            return

        light = Light(None, light_message=light_message)
        self.callback(light)

    def handle_cover(self, client: WebSocketClientProtocol, message):
        cover_message: CoverMessage
        try:
            cover_message = CoverMessage.model_validate_json(message)
        except ValidationError as e:
            print(f"SERVER ERROR -> {message}")
            self.send_error(client, ErrorCode.INVALID_DATA,
                            "Invalid cover data")
            return

        cover = Cover(cover_message=cover_message)
        self.callback(cover)
