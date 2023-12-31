from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel


class LigthAttributes(BaseModel):
    friendly_name: Optional[str] = None
    supported_features: Optional[int] = None
    brightness: Optional[int] = None
    color_mode: Optional[str] = None
    effect: Optional[str] = None
    effect_list: Optional[List[str]] = None
    hs_color: Optional[List[float]] = None
    min_color_temp_kelvin: Optional[int] = None
    max_color_temp_kelvin: Optional[int] = None
    color_temp_kelvin: Optional[int] = None
    min_mireds: Optional[int] = None
    max_mireds: Optional[int] = None
    rgb_color: Optional[List[int]] = None
    rgbww_color: Optional[List[int]] = None
    supported_color_modes: Optional[List[str]] = None
    icon: Optional[str] = None


class CoverAttributes(BaseModel):
    friendly_name: Optional[str] = None
    device_class: Optional[str] = None
    supported_features: Optional[int] = None
    current_position: Optional[int] = None
    current_tilt_position: Optional[int] = None


class SwitchAttributes(BaseModel):
    friendly_name: Optional[str] = None
    icon: Optional[str] = None
    state: str = "off"


class WeatherForecast(BaseModel):
    condition: str
    datetime: str
    wind_bearing: Optional[float] = None
    temperature: Optional[float] = None
    templow: Optional[float] = None
    wind_speed: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None


class WeatherAttributes(BaseModel):
    friendly_name: str
    attribution: Optional[str] = None
    temperature: Optional[float] = None
    dew_point: Optional[float] = None
    temperature_unit: Optional[str] = None
    humidity: Optional[float] = None
    cloud_coverage: Optional[float] = None
    pressure: Optional[float] = None
    pressure_unit: Optional[str] = None
    wind_bearing: Optional[float] = None
    wind_speed: Optional[float] = None
    wind_speed_unit: Optional[str] = None
    visibility_unit: Optional[str] = None
    precipitation_unit: Optional[str] = None
    forecast: List[WeatherForecast] = list()
    supported_features: int


class SensorAttributes(BaseModel):
    state_class: Optional[str] = None
    battery_level: Optional[int] = None
    unit_of_measurement: Optional[str] = None
    icon: Optional[str] = None
    device_class: Optional[str] = None
    friendly_name: Optional[str] = None


class HaEventState(BaseModel):
    entity_id: str
    state: str
    attributes: Dict[str, Any]


class HaEventData(BaseModel):
    entity_id: str
    new_state: HaEventState


class HaEvent(BaseModel):
    event_type: str
    data: HaEventData


class Result(BaseModel):
    entity_id: str
    state: str
    attributes: Dict[str, Any]
    last_changed: str
    last_updated: str


class HaIncomeMessage(BaseModel):
    id: Optional[int] = None
    type: str
    event: Optional[HaEvent] = None
    result: Optional[Any] = None
