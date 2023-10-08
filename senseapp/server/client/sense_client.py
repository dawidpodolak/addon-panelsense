import json

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
    websocket: WebSocketClientProtocol

    def __init__(self, websocket: WebSocketClientProtocol):
        super().__init__()
        self.websocket = websocket

    def set_client_data(self, auth_message: AuthenticationIncomingMessage):
        self.details = SenseClienDetails(
            name=auth_message.data.name,
            version_name=auth_message.data.version_name,
            version_code=auth_message.data.version_code,
            installation_id=auth_message.data.installation_id,
        )

    async def send(self, message: str):
        await self.websocket.send(message)

    def get_sense_client_json(self) -> str:
        return self.details.model_dump_json()
