from typing import Set

from client.sense_client import SenseClient


class ClientConectionCallback:
    def get_conntected_client(self) -> Set[SenseClient]:
        return set()

    def on_client_connect(self, client, SenseClient):
        pass

    def on_client_disconnect(self, client, SenseClient):
        pass
