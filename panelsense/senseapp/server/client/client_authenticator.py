import base64
import json
from typing import Callable, Optional, Set

from loguru import logger
from server.client.sense_client import SenseClient
from server.database.sense_database import SenseDatabase
from server.model.authentication import *
from server.model.server_credentials import ServerCredentials
from websockets.client import WebSocketClientProtocol


class AuthenticationError(Exception):
    pass


class ClientAuthenticator:
    encoded_credentials: str
    database: SenseDatabase

    def __init__(self, server_credentials: ServerCredentials, database: SenseDatabase):
        self.database = database
        self.user_name = server_credentials.username
        self.password = server_credentials.password
        self.encoded_credentials = base64.b64encode(
            f"{self.user_name}:{self.password}".encode("utf-8")
        ).decode("utf-8")

    async def authenticate(
        self,
        message: str,
        websocket: WebSocketClientProtocol,
        client_callback: Callable[[], Set[SenseClient]],
    ) -> Optional[SenseClient]:
        logger.info(f"Authenticating client with message: {message}")
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
            sense_client = next(
                (
                    client
                    for client in client_callback()
                    if client.details.installation_id
                    == auth_message.data.installation_id
                ),
                None,
            )
            logger.info(f"authentication: sense client found: {sense_client != None}")
            if not sense_client:
                logger.info(f"create new sense client")
                sense_client = SenseClient()

            sense_client.set_websocket(websocket)
            sense_client.set_client_data(auth_message)
            self.database.create_or_update_sense_client(sense_client)
            await websocket.send(
                AuthenticationRespone(
                    data=AuthResponseData(auth_result=AuthResult.SUCCESS)
                ).model_dump_json(exclude_none=True)
            )
            try:
                await sense_client.send_config()
            except Exception as e:
                logger.error(e)
            return sense_client
        else:
            await websocket.send(
                AuthenticationRespone(
                    data=AuthResponseData(auth_result=AuthResult.SUCCESS)
                ).model_dump_json(exclude_none=True)
            )
            return None

    def _is_authenticated(self, auth_message: AuthenticationIncomingMessage) -> bool:
        logger.info(
            f"Authenticating client with message: {auth_message} == {self.encoded_credentials}"
        )
        return auth_message.data.token == self.encoded_credentials
