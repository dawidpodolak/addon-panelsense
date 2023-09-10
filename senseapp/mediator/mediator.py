from homeassistant.home_assistant_client import HomeAssistantClient
from homeassistant.model.ha_message import HaEventData
from server.sense_server import PanelSenseServer
from mediator.components.light.light_component import Light
from mediator.components.base_component import BaseComponent


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

    def home_assistant_client_income_message_callback(self, message: HaEventData):
        domain = message.entity_id.split('.')[0]
        if domain == 'light':
            light = Light(message)
            self.sense_server.send_message(light)
        print(f"ha_client_message_callback: {message}")

    def server_client_income_message_callbck(self, message):
        self.home_assistnat_client.send_data(message.getHomeAssistantMessage())
        print(f"server_client_message_callbck: {message}")
