from pydantic import BaseModel
from typing import Optional, List


class LightState(BaseModel):

    on: bool = False
    brightness: Optional[int] = None
    color_mode: Optional[str] = None
    effect: Optional[str] = None
    effect_list: Optional[List[str]] = None
    friendly_name: Optional[str] = None
    hs_color: Optional[List[float]] = None
    min_color_temp_kelvin: Optional[int] = None
    max_color_temp_kelvin: Optional[int] = None
    min_mireds: Optional[int] = None
    max_mireds: Optional[int] = None
    rgb_color: Optional[List[int]] = None
    supported_color_modes: Optional[List[str]] = None
    supported_features: Optional[int] = None
