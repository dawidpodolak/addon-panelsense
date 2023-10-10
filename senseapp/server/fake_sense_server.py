import asyncio
from asyncio import AbstractEventLoop
from typing import List

from loging.logger import _LOGGER
from server.client.sense_client import SenseClienDetails, SenseClient
from server.client_connection_helper import ClientConectionHelper
from server.database.sense_database import SenseDatabase
from server.model.authentication import AuthData, AuthenticationIncomingMessage
from server.model.base import MessageType
from server.model.configuration import *


class FakeSenseServer(ClientConectionHelper):
    database: SenseDatabase

    def __init__(self, loop: AbstractEventLoop, database: SenseDatabase):
        self.database = database
        database.get_sense_clients()
        self.add_fake_client("Test android devices", "test Ad inId")
        loop.create_task(self.add_fake_client_with_delay())

    def add_fake_client(self, name: str, installation_id: str):
        fake_sense_client = SenseClient()
        fake_sense_client.set_configuration(self.get_configuration())
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
        self.database.create_or_update_sense_client(fake_sense_client)

    async def add_fake_client_with_delay(self):
        await asyncio.sleep(5)
        _LOGGER.debug("Add delayed fake client")
        self.add_fake_client("Test android 2", "Test androd idID")

    def get_configuration(self) -> Configuration:
        system_configuration = ConfigurationSystem(main_panel_id="button_panel")
        item_list: List[ConfigurationItem] = list()
        item_configuration: ConfigurationItem = ConfigurationItem(
            id="button_1",
            entity_id="cover.button",
        )
        item_list.append(item_configuration)
        item_list.append(item_configuration)
        item_list.append(item_configuration)
        item_list.append(item_configuration)

        panel = ConfigurationPanel(
            id="button_panel",
            type="grid",
            column_count=2,
            item_list=item_list,
        )
        panel_list: List[ConfigurationPanel] = list()
        panel_list.append(panel)
        return Configuration(system=system_configuration, panel_list=panel_list)
