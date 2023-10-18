from typing import Callable, Set

from server.client.sense_client import SenseClient


class ClientConectionHelper:
    connected_clients: Set[SenseClient] = set()
    client_connected_callbacks: Set[Callable[[SenseClient], None]] = set()
    client_diconnected_callbacks: Set[Callable[[SenseClient], None]] = set()

    def on_client_connected(self, client: SenseClient):
        if client not in self.connected_clients:
            client.is_online = True
            self.connected_clients.add(client)
        else:
            for sense_client in self.connected_clients:
                if (
                    sense_client.details.installation_id
                    == client.details.installation_id
                ):
                    sense_client.is_online = True

        for callback in self.client_connected_callbacks:
            callback(client)

    def on_client_disconnected(self, client: SenseClient):
        for sense_client in self.connected_clients:
            if sense_client.details.installation_id == client.details.installation_id:
                sense_client.is_online = False

        for callback in self.client_diconnected_callbacks:
            callback(client)

    def update_sense_client_config(self, installation_id: str, config: str):
        pass
