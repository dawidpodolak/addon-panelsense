from enum import Enum
from typing import List, Optional, Set

from pydantic import BaseModel


class ConfigurationSystem(BaseModel):
    main_panel_id: Optional[str] = None


class ConfigurationItem(BaseModel):
    id: str
    entity_id: str
    title: Optional[str] = None
    icon: Optional[str] = None
    background: Optional[str] = None

    def __hash__(self):
        return hash(self.id)


class ConfigurationPanelType(Enum):
    HOME = "home"
    GRID = "grid"


class ConfigurationPanel(BaseModel):
    id: str
    type: str
    column_count: int = 1
    background: Optional[str] = None
    item_list: List[ConfigurationItem] = list()

    def __hash__(self):
        return hash(self.id)

    # def model_dump1(self):
    #     dict = self.model_dump()
    #     dict["type"] = self.type.value
    #     return dict


class Configuration(BaseModel):
    system: ConfigurationSystem
    panel_list: List[ConfigurationPanel] = list()
