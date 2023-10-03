import base64
import json
from typing import Optional

from loging.logger import _LOGGER
from server.client.sense_client import SenseClient
from server.model.authentication import *
from server.model.server_credentials import ServerCredentials
from websockets.client import WebSocketClientProtocol


class AuthenticationError(Exception):
    pass


class ClientAuthenticator:
    encoded_credentials: str

    def __init__(self, server_credentials: ServerCredentials):
        self.user_name = server_credentials.username
        self.password = server_credentials.password
        self.encoded_credentials = base64.b64encode(
            f"{self.user_name}:{self.password}".encode("utf-8")
        ).decode("utf-8")

    async def authenticate(
        self, message: str, websocket: WebSocketClientProtocol
    ) -> Optional[SenseClient]:
        print(f"Authenticating client with message: {message}")
        auth_message: AuthenticationIncomingMessage
        try:
            auth_message = AuthenticationIncomingMessage.model_validate_json(message)
        except Exception as e:
            await websocket.send(
                AuthenticationRespone(
                    data=AuthResponseData(auth_result=AuthResult.FAILURE)
                ).model_dump_json(exclude_none=True)
            )
            return None

        if self._is_authenticated(auth_message):
            sense_client = SenseClient(websocket)
            sense_client.set_client_data(auth_message)
            await websocket.send(
                AuthenticationRespone(
                    data=AuthResponseData(auth_result=AuthResult.SUCCESS)
                ).model_dump_json(exclude_none=True)
            )
            return sense_client
        else:
            await websocket.send(
                AuthenticationRespone(
                    data=AuthResponseData(auth_result=AuthResult.SUCCESS)
                ).model_dump_json(exclude_none=True)
            )
            return None

    def _is_authenticated(self, auth_message: AuthenticationIncomingMessage) -> bool:
        print(
            f"Authenticating client with message: {auth_message} == {self.encoded_credentials}"
        )
        return auth_message.data.token == self.encoded_credentials
