from homeassistant import hassApi
import asyncio

loop = asyncio.get_event_loop()


async def listening_user_input():
    print(f"Listening for input")
    while True:
        user_input = input("Wpisz coś\n")
        loop.create_task(hassApi.send_data(user_input))


def setup():

    loop.create_task(hassApi.start_websocket())
    # loop.run_until_complete(listening_user_input())
    loop.run_forever()


setup()
