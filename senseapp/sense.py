import argparse
import asyncio
import os
import sys
import threading

from homeassistant.components.event_observer import EventObserver
from homeassistant.home_assistant_client import HomeAssistantClient
from loging.logger import _LOGGER
from mediator.mediator import Mediator
from server.client_connection_helper import ClientConectionHelper
from server.database.sense_database import SenseDatabase
from server.fake_sense_server import FakeSenseServer
from server.model.server_credentials import ServerCredentials
from server.sense_server import PanelSenseServer
from ui.dashboard import *

parser = argparse.ArgumentParser(description="Start the application")
parser.add_argument("--debugUI", action="store_true", help="Enable debug UI")
args = parser.parse_args()

loop = asyncio.get_event_loop()
mediator: Mediator
client_connection_helper: ClientConectionHelper
database = SenseDatabase()


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
    if args.debugUI:
        setup_fake_server()
    else:
        server_thread = threading.Thread(target=setup_real_server)
        server_thread.start()


def setup_real_server():
    global client_connection_helper

    ha_event_observer = EventObserver()
    ha_client = HomeAssistantClient(loop, ha_event_observer)
    panel_sense_server = PanelSenseServer(loop, get_server_credentails(), database)
    client_connection_helper = panel_sense_server
    mediator = Mediator(ha_client, panel_sense_server)
    loop.run_forever()


def setup_fake_server():
    global client_connection_helper
    client_connection_helper = FakeSenseServer(loop, database)


def sense_serve_callback() -> ClientConectionHelper:
    global client_connection_helper
    return client_connection_helper


def main():
    setup_server()
    start_web_app(args.debugUI, server_callback=sense_serve_callback)


if __name__ == "__main__":
    main()
