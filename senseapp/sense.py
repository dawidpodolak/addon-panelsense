import asyncio
import sys

from homeassistant.components.event_observer import EventObserver
from homeassistant.home_assistant_client import HomeAssistantClient
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


def main():
    ha_event_observer = EventObserver()
    ha_client = HomeAssistantClient(loop, ha_event_observer)
    server_credentials = ServerCredentials("admin", "admin")
    panel_sense_server = PanelSenseServer(loop, server_credentials)
    mediator = Mediator(ha_client, panel_sense_server)
    # loop.create_task(listening_user_input())
    loop.run_forever()


if __name__ == "__main__":
    main()
