from server.model.authentication import AuthenticationIncomingMessage
from websockets.client import WebSocketClientProtocol


class SenseClient:
    name: str
    version_name: str
    version_code: int
    websocket: WebSocketClientProtocol

    def __init__(self, websocket: WebSocketClientProtocol):
        super().__init__()
        self.websocket = websocket

    def set_client_data(self, auth_message: AuthenticationIncomingMessage):
        self.name = auth_message.data.name
        self.version_name = auth_message.data.version_name
        self.version_code = auth_message.data.version_code

    async def send(self, message: str):
        await self.websocket.send(message)
