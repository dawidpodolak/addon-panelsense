import asyncio
import websockets


SENSE_SERVER_PORT = 8652


async def message_handler(websocket):
    async for message in websocket:
        print(f"Reveived message:\n {message}")


async def start_sense_server():
    print(f"Server starting at ws://localhost:{SENSE_SERVER_PORT}")
    async with websockets.serve(message_handler, "0.0.0.0", SENSE_SERVER_PORT):
        print(f"Server started at ws://localhost:{SENSE_SERVER_PORT}")
        await asyncio.Future()
