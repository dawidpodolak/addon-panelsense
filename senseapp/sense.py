import asyncio
import os
import sys
import threading

from ui.dashboard import *
from homeassistant.components.event_observer import EventObserver
from homeassistant.home_assistant_client import HomeAssistantClient
from loging.logger import _LOGGER
from mediator.mediator import Mediator
from server.model.server_credentials import ServerCredentials
from server.sense_server import PanelSenseServer

loop = asyncio.get_event_loop()
mediator: Mediator


async def get_steam_reader(pipe) -> str:
    reader = asyncio.StreamReader(loop=loop)
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, pipe)
    line = await reader.readline()

    return line.decode("utf-8").rstrip("\n")


async def listening_user_input():
    while True:
        user_input = await get_steam_reader(sys.stdin)


def get_server_credentails() -> ServerCredentials:
    server_credentials = ServerCredentials("admin", "admin")
    env_server_user = os.getenv("OPTIONS_SERVER_USER")
    env_server_password = os.getenv("OPTIONS_SERVER_PASSWORD")

    if env_server_user:
        server_credentials.username = env_server_user

    if env_server_password:
        server_credentials.password = env_server_password

    _LOGGER.debug(
        f"Credentials: user: {server_credentials.username}, pswd: {server_credentials.password}"
    )
    return server_credentials

def setup_server():
    ha_event_observer = EventObserver()
    ha_client = HomeAssistantClient(loop, ha_event_observer)
    panel_sense_server = PanelSenseServer(loop, get_server_credentails())
    mediator = Mediator(ha_client, panel_sense_server)
    loop.run_forever()

def main():
    server_thread = threading.Thread(target=setup_server)
    server_thread.start()
    start_web_app()

if __name__ == "__main__":
    main()
