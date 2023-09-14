from homeassistant.home_assistant_client import HomeAssistantClient
from homeassistant.model.ha_income_message import HaEventData
from mediator.components.base_component import BaseComponent
from mediator.components.cover.cover_component import Cover
from mediator.components.light.light_component import Light
from server.sense_server import PanelSenseServer


class Mediator:

    home_assistnat_client: HomeAssistantClient
    sense_server: PanelSenseServer

    def __init__(self, ha_client: HomeAssistantClient, sense_server: PanelSenseServer):
        self.home_assistnat_client = ha_client
        self.home_assistnat_client.set_message_callback(
            self.home_assistant_client_income_message_callback)
        self.sense_server = sense_server
        self.sense_server.set_message_callback(
            self.server_client_income_message_callbck)

    def home_assistant_client_income_message_callback(self, component: BaseComponent):
        self.sense_server.send_message(component)

    def server_client_income_message_callbck(self, message):
        self.home_assistnat_client.send_data(message.getHomeAssistantMessage())
        print(f"server_client_message_callbck: {message}")
