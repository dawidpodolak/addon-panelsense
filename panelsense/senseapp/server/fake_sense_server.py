import asyncio
from asyncio import AbstractEventLoop
from typing import List

from loguru import logger
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
        self.connected_clients = database.get_sense_clients()
        logger.info(f"Init FakeSenseServer with {len(self.connected_clients)} clients")
        # self.add_fake_client("Test android devices", "test Ad inId")
        # loop.create_task(self.add_fake_client_with_delay())

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
        self.on_client_connected(fake_sense_client)
        self.database.create_or_update_sense_client(fake_sense_client)

    async def add_fake_client_with_delay(self):
        await asyncio.sleep(5)
        logger.debug("Add delayed fake client")
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

    def update_sense_client_config(self, installation_id: str, config: str):
        sense_client: Optional[SenseClient] = None

        for sc in self.connected_clients:
            if sc.details.installation_id == installation_id:
                sense_client = sc

        logger.info(f"Updadate sense client {installation_id} with config: {config}")
        if sense_client:
            sense_client.configuration_str = config
            self.database.update_sense_client_configuration(installation_id, config)
