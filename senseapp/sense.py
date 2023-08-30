from homeassistant import hass_ws_client
from server import sense_server
import asyncio

loop = asyncio.get_event_loop()


async def listening_user_input():
    print(f"Listening for input")
    while True:
        user_input = input("Wpisz coś\n")
        loop.create_task(hass_ws_client.send_data(user_input))

if __name__ == "__main__":
    loop.create_task(hass_ws_client.start_haws_client())
    loop.create_task(sense_server.start_sense_server())
    # loop.run_until_complete(listening_user_input())
    loop.run_forever()
