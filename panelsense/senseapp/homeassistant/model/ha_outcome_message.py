from typing import List, Optional, Union

from pydantic import BaseModel


class LightServiceData(BaseModel):
    color_name: Optional[str] = None
    color_mode: Optional[str] = None
    rgb_color: Optional[List[int]] = None
    color_temp_kelvin: Optional[int] = None
    brightness: Optional[int] = None
    position: Optional[int] = None


class CoverServiceData(BaseModel):
    position: Optional[int] = None


class Target(BaseModel):
    entity_id: str


class HaOutcomeMessage(BaseModel):
    id: Optional[int] = None
    type: str
    domain: Optional[str] = None


class HaCallServiceMessage(HaOutcomeMessage):
    type: str = "call_service"
    domain: str
    service: str
    service_data: Optional[Union[CoverServiceData, LightServiceData]] = None
    target: Optional[Target] = None
