from typing import Callable, Set

from server.client.sense_client import SenseClient


class ClientConectionHelper:
    connected_clients: Set[SenseClient] = set()
    client_connected_callbacks: Set[Callable[[SenseClient], None]] = set()
    client_diconnected_callbacks: Set[Callable[[SenseClient], None]] = set()

    def add_client(self, client: SenseClient):
        self.connected_clients.add(client)
        for callback in self.client_connected_callbacks:
            callback(client)

    def remove_client(self, client: SenseClient):
        self.connected_clients.remove(client)
        for callback in self.client_diconnected_callbacks:
            callback(client)

    def update_sense_client_config(self, installation_id: str, config: str):
        pass
