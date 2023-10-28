from homeassistant.ids import get_message_id
from homeassistant.model.ha_income_message import (HaEventData,
                                                   WeatherAttributes)
from homeassistant.model.ha_outcome_message import *
from loguru import logger
from server.model.weather import *

from .base_component import BaseComponent


class Weather(BaseComponent):
    entity: str
    state: str
    weather_attributes: WeatherAttributes

    def __init__(self, ha_event_data: HaEventData):
        logger.debug(f"WEATHER -->> {ha_event_data.model_dump_json()}")
        self.entity = ha_event_data.entity_id
        self.state = ha_event_data.new_state.state
        self.weather_attributes = WeatherAttributes(
            **ha_event_data.new_state.attributes
        )

    def get_message_for_client(self) -> ServerOutgoingMessage:
        return WeatherOutcomingMessage(data=self.get_data())

    def get_data(self) -> WeatherOutcomingDataMessage:
        return WeatherOutcomingDataMessage(
            forecast=self.get_forecast_list(),
            entity_id=self.entity,
            state=self.state,
            temperature=self.weather_attributes.temperature,
            dew_point=self.weather_attributes.dew_point,
            temperature_unit=self.weather_attributes.temperature_unit,
            humidity=self.weather_attributes.humidity,
            cloud_coverage=self.weather_attributes.cloud_coverage,
            pressure=self.weather_attributes.pressure,
            pressure_unit=self.weather_attributes.pressure_unit,
            wind_bearing=self.weather_attributes.wind_bearing,
            wind_speed_unit=self.weather_attributes.wind_speed_unit,
            visibility_unit=self.weather_attributes.visibility_unit,
            precipitation_unit=self.weather_attributes.precipitation_unit,
            friendly_name=self.weather_attributes.friendly_name,
            supported_features=self.weather_attributes.supported_features,
            attribution=self.weather_attributes.attribution,
        )

    def get_forecast_list(self) -> List[WeatherForecast]:
        forecast_list: List[WeatherForecast] = list()

        for ha_forecast in self.weather_attributes.forecast:
            forecast_list.append(
                WeatherForecast(
                    condition=ha_forecast.condition,
                    datetime=ha_forecast.datetime,
                    wind_bearing=ha_forecast.wind_bearing,
                    temperature=ha_forecast.temperature,
                    templow=ha_forecast.templow,
                    wind_speed=ha_forecast.wind_speed,
                    humidity=ha_forecast.humidity,
                )
            )
        return forecast_list
