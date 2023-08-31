import json
from homeassistant.ids import get_message_id
from homeassistant import hass_ws_client

DOMAIN = "light"
MESSAGE_TYPE = "call_service"
TURN_ON_SERVICE = "turn_on"
TURN_OFF_SERVICE = "turn_off"
SWITCH_SERVICE = "toggle"

data = {
    "domain": "light",
    "type": MESSAGE_TYPE,
}
target = {}


def get_entity_data(entity="", domain=DOMAIN):
    final_target = {"entity_id": entity}
    data["target"] = final_target
    data["id"] = get_message_id()
    data["domain"] = domain
    return data


async def turn_light_on(entity):
    data_to_send = get_entity_data(entity)
    data_to_send["service"] = TURN_ON_SERVICE
    await hass_ws_client.send_data(json.dumps(data_to_send))


async def turn_light_off(entity):
    data_to_send = get_entity_data(entity)
    data_to_send["service"] = TURN_OFF_SERVICE
    await hass_ws_client.send_data(json.dumps(data_to_send))


async def toggle_light(entity):
    data_to_send = get_entity_data(entity)
    data_to_send["service"] = SWITCH_SERVICE
    await hass_ws_client.send_data(json.dumps(data_to_send))
