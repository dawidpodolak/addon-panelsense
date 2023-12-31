from typing import Optional

from homeassistant.ids import get_message_id
from homeassistant.model.ha_income_message import HaEventData, LigthAttributes
from homeassistant.model.ha_outcome_message import *
from loguru import logger
from mediator.components.base_component import BaseComponent
from server.model.light import *


class Light(BaseComponent):
    on: bool = False
    brightness: Optional[int] = 0
    color_mode: Optional[str] = None
    rgb_color: Optional[List[int]] = None
    rgbww_color: Optional[List[int]] = None
    color_temp_kelvin: Optional[int] = None
    supported_color_modes: Optional[List[str]] = None
    friendly_name: Optional[str] = None
    min_color_temp_kelvin: Optional[int] = None
    max_color_temp_kelvin: Optional[int] = None
    icon: Optional[str] = None
    supported_features: Optional[int] = None

    def __init__(
        self,
        haEventData: Optional[HaEventData] = None,
        light_incoming_message: Optional[LightIncomingMessage] = None,
    ):
        if haEventData:
            self.updateState(haEventData)
        elif light_incoming_message:
            self.update_state_from_server(light_incoming_message.data)

    def updateState(self, haEventData: HaEventData):
        attributes = LigthAttributes(**haEventData.new_state.attributes)
        self.entity_id = haEventData.entity_id
        self.on = haEventData.new_state.state == "on"
        self.brightness = attributes.brightness
        self.color_mode = attributes.color_mode
        self.effect = attributes.effect
        self.effect_list = attributes.effect_list
        self.friendly_name = attributes.friendly_name
        self.hs_color = attributes.hs_color
        self.min_color_temp_kelvin = attributes.min_color_temp_kelvin
        self.max_color_temp_kelvin = attributes.max_color_temp_kelvin
        self.color_temp_kelvin = attributes.color_temp_kelvin
        self.min_mireds = attributes.min_mireds
        self.max_mireds = attributes.max_mireds
        self.rgb_color = attributes.rgb_color
        self.rgbww_color = attributes.rgbww_color
        self.supported_color_modes = attributes.supported_color_modes
        self.supported_features = attributes.supported_features
        self.icon = attributes.icon

    def get_message_for_home_assistant(self) -> HaOutcomeMessage:
        return HaCallServiceMessage(
            id=get_message_id(),
            domain="light",
            service=self.get_ha_service(),
            service_data=self.get_service_data(),
            target=Target(entity_id=self.entity_id),
        )

    def get_message_for_client(self) -> LightOutcomingMessage:
        data = LightOutcomingDataMessage(
            entity_id=self.entity_id,
            on=self.on,
            brightness=self.brightness,
            color_mode=self.color_mode,
            rgb_color=self.rgb_color,
            rgbww_color=self.rgbww_color,
            supported_color_modes=self.supported_color_modes,
            max_color_temp_kelvin=self.max_color_temp_kelvin,
            min_color_temp_kelvin=self.min_color_temp_kelvin,
            color_temp_kelvin=self.color_temp_kelvin,
            friendly_name=self.friendly_name,
            icon=self.icon,
            supported_features=self.supported_features,
        )
        return LightOutcomingMessage(data=data)

    def update_state_from_server(
        self, light_incoming_message: LightIncomingDataMessage
    ):
        self.entity_id = light_incoming_message.entity_id
        self.on = light_incoming_message.on
        self.brightness = light_incoming_message.brightness
        self.color_mode = light_incoming_message.color_mode
        self.rgb_color = light_incoming_message.rgb_color
        self.rgbww_color = light_incoming_message.rgbww_color
        self.color_temp_kelvin = light_incoming_message.color_temp_kelvin
        self.supported_color_modes = light_incoming_message.supported_color_modes
        self.max_color_temp_kelvin = light_incoming_message.max_color_temp_kelvin
        self.min_color_temp_kelvin = light_incoming_message.min_color_temp_kelvin
        self.color_temp_kelvin = light_incoming_message.color_temp_kelvin

    def get_ha_service(self) -> str:
        if self.on:
            return "turn_on"
        else:
            return "turn_off"

    def get_service_data(self) -> Optional[LightServiceData]:
        if self.brightness or self.color_mode or self.rgb_color:
            return LightServiceData(
                rgb_color=self.rgb_color,
                rgbww_color=self.rgbww_color,
                brightness=self.brightness,
                color_temp_kelvin=self.color_temp_kelvin,
            )
        else:
            return None
