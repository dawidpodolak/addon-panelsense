from homeassistant.home_assistant_client import HomeAssistantClient
from server.sense_server import PanelSenseServer
from homeassistant.components.event_observer import EventObserver
from mediator.mediator import Mediator
import asyncio
import sys

loop = asyncio.get_event_loop()
mediator: Mediator


async def get_steam_reader(pipe) -> str:
    reader = asyncio.StreamReader(loop=loop)
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, pipe)
    line = await reader.readline()

    return line.decode('utf-8').rstrip('\n')


async def listening_user_input():
    while True:
        user_input = await get_steam_reader(sys.stdin)


def main():
    ha_event_observer = EventObserver()
    ha_client = HomeAssistantClient(loop, ha_event_observer)
    panel_sense_server = PanelSenseServer(loop)
    mediator = Mediator(ha_client, panel_sense_server)
    loop.create_task(listening_user_input())
    loop.run_forever()


if __name__ == "__main__":
    main()
