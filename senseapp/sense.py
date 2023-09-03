from homeassistant.hass_ws_client import HomeAssistantClient
from homeassistant.components.light import *
from server.sense_server import PanelSenseServer
from homeassistant.components.event_observer import EventObserver
import asyncio
import sys

loop = asyncio.get_event_loop()


async def get_steam_reader(pipe) -> str:
    reader = asyncio.StreamReader(loop=loop)
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, pipe)
    line = await reader.readline()

    return line.decode('utf-8').rstrip('\n')


async def listening_user_input():
    while True:
        user_input = await get_steam_reader(sys.stdin)
        if user_input == '1':
            await turn_light_on("light.bed_light")
        elif user_input == '2':
            await turn_light_off("light.bed_light")
        elif user_input == '3':
            await toggle_light("light.bed_light")


def main():
    ha_event_observer = EventObserver()
    haClient = HomeAssistantClient(loop, ha_event_observer)
    panelSenseSrver = PanelSenseServer(loop)
    loop.create_task(listening_user_input())
    loop.run_forever()


if __name__ == "__main__":
    main()
