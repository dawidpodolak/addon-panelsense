import asyncio
import websockets
from asyncio import AbstractEventLoop


class PanelSenseServer:

    def __init__(self, loop: AbstractEventLoop):
        loop.create_task(self.start_sense_server())

    SENSE_SERVER_PORT = 8652

    async def message_handler(self, websocket):
        async for message in websocket:
            print(f"Reveived message:\n {message}")

    async def start_sense_server(self):
        print(f"Server starting at ws://localhost:{self.SENSE_SERVER_PORT}")
        async with websockets.serve(self.message_handler, "0.0.0.0", self.SENSE_SERVER_PORT):
            print(f"Server started at ws://localhost:{self.SENSE_SERVER_PORT}")
            await asyncio.Future()
