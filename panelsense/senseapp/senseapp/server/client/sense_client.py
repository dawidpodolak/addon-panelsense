from typing import Optional

import yaml
from loging.logger import _LOGGER
from pydantic import BaseModel
from server.model.authentication import AuthenticationIncomingMessage
from server.model.configuration import (Configuration,
                                        ConfigurationOutcomingMessage)
from websockets.client import WebSocketClientProtocol


class SenseClienDetails(BaseModel):
    name: str
    version_name: str
    version_code: int
    installation_id: str  # base64

    def __hash__(self):
        return hash((self.installation_id,))


class SenseClient:
    details: SenseClienDetails
    websocket: Optional[WebSocketClientProtocol] = None
    configuration_str: str = "system:\npanel_item:"
    is_online = False

    def set_configuration(self, configuration: Configuration):
        self.configuration = configuration

    def set_websocket(self, websocket: WebSocketClientProtocol):
        self.websocket = websocket

    def clear_websocket(self):
        self.websocket = None

    def is_connectect(self) -> bool:
        if self.websocket:
            return True
        else:
            return False

    def set_client_data(self, auth_message: AuthenticationIncomingMessage):
        self.details = SenseClienDetails(
            name=auth_message.data.name,
            version_name=auth_message.data.version_name,
            version_code=auth_message.data.version_code,
            installation_id=auth_message.data.installation_id,
        )

    async def send(self, message: str):
        if self.websocket:
            await self.websocket.send(message)

    def get_sense_client_json(self) -> str:
        return self.details.model_dump_json()

    def get_configuration(self):
        return self.configuration_str

    async def send_config(self):
        try:
            yaml_config = yaml.safe_load(self.configuration_str)
            configuration_message = ConfigurationOutcomingMessage(
                data=Configuration(**yaml_config)
            )
            _LOGGER.info(
                f"Client <- Send configuration to device: -> {configuration_message.model_dump_json(exclude_none=True)}"
            )
            if self.websocket:
                await self.websocket.send(
                    configuration_message.model_dump_json(exclude_none=True)
                )
        except Exception as e:
            _LOGGER.error(e)


def create_sense_client(
    name: str,
    installation_id: str,
    version_name: str,
    version_code: int,
    configuration: str,
) -> SenseClient:
    details = SenseClienDetails(
        name=name,
        installation_id=installation_id,
        version_name=version_name,
        version_code=version_code,
    )
    sense_client = SenseClient()
    sense_client.configuration_str = configuration
    sense_client.details = details
    return sense_client
