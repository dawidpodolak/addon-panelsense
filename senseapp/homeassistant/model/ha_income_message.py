from typing import List, Optional

from pydantic import BaseModel


class StateAttributes(BaseModel):
    # common attributes
    friendly_name: Optional[str] = None
    supported_features: Optional[int] = None

    # light attributes
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
    supported_color_modes: Optional[List[str]] = None

    # cover attributes
    current_position: Optional[int] = None


class HaEventState(BaseModel):
    entity_id: str
    state: str
    attributes: StateAttributes


class HaEventData(BaseModel):
    entity_id: str
    new_state: HaEventState


class HaEvent(BaseModel):
    event_type: str
    data: HaEventData


class HaIncomeMessage(BaseModel):
    id: Optional[int] = None
    type: str
    event: Optional[HaEvent] = None
