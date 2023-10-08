import asyncio
from asyncio import AbstractEventLoop

from loging.logger import _LOGGER
from server.client.sense_client import SenseClienDetails, SenseClient
from server.client_connection_helper import ClientConectionHelper
from server.model.authentication import AuthData, AuthenticationIncomingMessage
from server.model.base import MessageType


class FakeSenseServer(ClientConectionHelper):
    def __init__(self, loop: AbstractEventLoop):
        self.add_fake_client("Test android devices", "test Ad inId")
        loop.create_task(self.add_fake_client_with_delay())

    def add_fake_client(self, name: str, installation_id: str):
        fake_sense_client = SenseClient()
        authIncomingMessage = AuthenticationIncomingMessage(
            type=MessageType.AUTH,
            data=AuthData(
                token="test token",
                name=name,
                version_code=1,
                version_name="0.1.0",
                installation_id=installation_id,
            ),
        )
        fake_sense_client.set_client_data(authIncomingMessage)
        self.add_client(fake_sense_client)

    async def add_fake_client_with_delay(self):
        await asyncio.sleep(5)
        _LOGGER.debug("Add delayed fake client")
        self.add_fake_client("Test android 2", "Test androd idID")
