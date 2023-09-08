import asyncio
import websockets
from websockets import WebSocketClientProtocol
from asyncio import AbstractEventLoop
from mediator.components.base_component import BaseComponent
import json


class PanelSenseServer:

    def __init__(self, loop: AbstractEventLoop):
        loop.create_task(self.start_sense_server())

    SENSE_SERVER_PORT = 8652

    websocket_server: WebSocketClientProtocol

    connected_clients = set()

    async def message_handler(self, websocket):
        self.connected_clients.add(websocket)
        async for message in websocket:
            print(f"Reveived message:\n {message}")

    async def start_sense_server(self):
        print(f"Server starting at ws://localhost:{self.SENSE_SERVER_PORT}")
        self.websocket_server = await websockets.serve(self.message_handler, "0.0.0.0", self.SENSE_SERVER_PORT)
        await self.websocket_server.serve_forever()
        # async with websockets.serve(self.message_handler, "0.0.0.0", self.SENSE_SERVER_PORT):
        #     print(f"Server started at ws://localhost:{self.SENSE_SERVER_PORT}")
        #     self.websocket_server = websockets
        # await asyncio.Future()

    async def send_message_async(self, message: BaseComponent):
        for client in self.connected_clients:
            await client.send(json.dumps(message.getSenseServerMessage().model_dump()))
            # await client.send("received message")
        # await self.websocket_server.send("received message")

    def send_message(self, message: BaseComponent):
        print(f"Sending message: {message.getSenseServerMessage()}")
        asyncio.create_task(self.send_message_async(message))
