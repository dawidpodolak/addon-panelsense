from server.client.sense_client import SenseClienDetails, SenseClient
from server.client_connection_helper import ClientConectionHelper
from server.model.authentication import AuthData, AuthenticationIncomingMessage
from server.model.base import MessageType


class FakeSenseServer(ClientConectionHelper):
    def __init__(self):
        fake_sense_client = SenseClient()
        authIncomingMessage = AuthenticationIncomingMessage(
            type=MessageType.AUTH,
            data=AuthData(
                token="test token",
                name="Test device",
                version_code=1,
                version_name="0.1.0",
                installation_id="asdkfasdjf",
            ),
        )
        fake_sense_client.set_client_data(authIncomingMessage)
        self.add_client(fake_sense_client)
