from homeassistant.hass_ws_client import HomeAssistantClient
from homeassistant.model.ha_message import HaEventData
from server.sense_server import PanelSenseServer
from mediator.components.light.light_1 import Light


class Mediator:

    ha_client: HomeAssistantClient
    sense_server: PanelSenseServer

    def __init__(self, ha_client: HomeAssistantClient, sense_server: PanelSenseServer):
        self.ha_client = ha_client
        self.ha_client.set_message_callback(self.ha_client_message_callback)
        self.sense_server = sense_server

    def ha_client_message_callback(self, message: HaEventData):
        domain = message.entity_id.split('.')[0]
        if domain == 'light':
            light = Light(message)
            self.sense_server.send_message(light)
        print(f"ha_client_message_callback: {message}")
