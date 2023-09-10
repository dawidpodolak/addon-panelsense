import asyncio
import websockets
from websockets import WebSocketClientProtocol
from asyncio import AbstractEventLoop
from mediator.components.base_component import BaseComponent
import json
from server.model.server_message import ServerMessage
from server.model.server_message import LightMessage
from mediator.components.light.light_component import Light
from typing import Callable


class PanelSenseServer:

    def __init__(self, loop: AbstractEventLoop):
        loop.create_task(self.start_sense_server())

    SENSE_SERVER_PORT = 8652

    websocket_server: WebSocketClientProtocol

    connected_clients = set()
    callback = None

    async def message_handler(self, websocket):
        self.connected_clients.add(websocket)
        async for message in websocket:
            self.handle_message(message)
            print(f"Reveived message:\n {message}")

    async def start_sense_server(self):
        print(f"Server starting at ws://localhost:{self.SENSE_SERVER_PORT}")
        self.websocket_server = await websockets.serve(self.message_handler, "0.0.0.0", self.SENSE_SERVER_PORT)
        await self.websocket_server.serve_forever()

    async def send_message_async(self, message: BaseComponent):
        for client in self.connected_clients:
            await client.send(json.dumps(message.getSenseServerMessage().model_dump()))

    def send_message(self, message: BaseComponent):
        print(f"Sending message: {message.getSenseServerMessage()}")
        # asyncio.create_task(self.send_message_async(message))

    def handle_message(self, message):
        server_message = ServerMessage.model_validate_json(message)
        domain = server_message.entity_id.split('.')[0]

        if domain == 'light':
            light_message = LightMessage.model_validate_json(message)
            print(
                f"handle light message: {light_message} ---->> {self.callback}")
            light = Light(None, light_message=light_message)
            self.callback(light)

    def set_message_callback(self, callback):
        self.callback = callback
