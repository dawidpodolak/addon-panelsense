from typing import List, Optional

from pydantic import BaseModel

from .base import *


class WeatherForecast(BaseModel):
    condition: str
    datetime: str
    wind_bearing: Optional[float] = None
    temperature: Optional[float] = None
    templow: Optional[float] = None
    wind_speed: Optional[float] = None
    humidity: Optional[float] = None


class WeatherOutcomingDataMessage(BaseModel):
    entity_id: str
    state: Optional[str] = None
    temperature: Optional[float] = None
    dew_point: Optional[float] = None
    temperature_unit: str
    humidity: Optional[float] = None
    cloud_coverage: Optional[float] = None
    pressure: Optional[float] = None
    pressure_unit: str
    wind_bearing: Optional[float] = None
    wind_speed_unit: str
    visibility_unit: str
    precipitation_unit: str
    forecast: List[WeatherForecast]
    friendly_name: str
    supported_features: int
    attribution: str


class WeatherOutcomingMessage(ServerOutgoingMessage):
    type: MessageType = MessageType.HA_ACTION_WEATHER
    data: WeatherOutcomingDataMessage
