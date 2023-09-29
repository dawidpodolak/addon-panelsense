from server.model.authentication import AuthenticationIncomingMessage
from websockets.client import WebSocketClientProtocol


class SenseClient(WebSocketClientProtocol):

    name: str
    version_name: str
    version_code: int

    def __init__(self, websocket: WebSocketClientProtocol):
        super().__init__()
        self.websocket = websocket

    def set_client_data(self, auth_message: AuthenticationIncomingMessage):
        self.name = auth_message.name
        self.version_name = auth_message.version_name
        self.version_code = auth_message.version_code
