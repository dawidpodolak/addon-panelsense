import json
from typing import Optional

from pydantic import BaseModel
from server.model.authentication import AuthenticationIncomingMessage
from websockets.client import WebSocketClientProtocol


class SenseClienDetails(BaseModel):
    name: str
    version_name: str
    version_code: int
    installation_id: str

    def __hash__(self):
        return hash((self.installation_id,))


class SenseClient:
    details: SenseClienDetails
    websocket: Optional[WebSocketClientProtocol] = None

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
