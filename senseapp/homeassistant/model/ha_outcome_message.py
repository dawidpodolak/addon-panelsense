from pydantic import BaseModel
from typing import List, Optional


class ServiceData(BaseModel):
    pass


class LightServiceData(ServiceData):
    color_name: Optional[str] = None
    color_mode: Optional[str] = None
    rgb_color: Optional[List[int]] = None
    color_temp_kelvin: Optional[int] = None
    brightness: Optional[int] = None


class Target(BaseModel):
    entity_id: str


class HaOutcomeMessage(BaseModel):
    id: Optional[int] = None
    type: str
    domain: str


class HaCallServiceMessage(HaOutcomeMessage):
    type: str = "call_service"
    domain: str
    service: str
    service_data: Optional[LightServiceData] = None
    target: Optional[Target] = None
