# import websocket
import json
import websockets
import logging
import asyncio
from homeassistant.auth_ha import auth
from homeassistant.state import subscribe_to_state

HOME_ASSISTANT_URL = "ws://172.30.32.1:8123/api/websocket"
websocket = None
MESSAGE_TYPE = "type"


async def start_websocket():
    global websocket
    logging.basicConfig(
        format="%(message)s",
        level=logging.DEBUG,
    )
    print(f"Starting websocket ....")
    websocket = await websockets.connect(HOME_ASSISTANT_URL)
    print(f"Websocket started!")

    response = await websocket.recv()
    await handle_message(response)
    print(f"response1: {response}")
    await subscribe_to_state(websocket)
    await listen_for_message()


async def listen_for_message():
    # while True:
    response = await websocket.recv()
    print(f"response2: {response}")


async def send_data(data):
    global websocket
    print(f"Send data: {data}")
    if websocket:
        print(f"Send data to websocket: {data}")
        await websocket.send(data)
    else:
        print(f"websocket not initializade")


async def handle_message(message):
    print(f"message: {message}")
    jsonData = json.loads(message)
    messageType = jsonData.get(MESSAGE_TYPE)
    print(f"messageType: {messageType}")
    if messageType == "auth_required":
        await auth(websocket, message)
