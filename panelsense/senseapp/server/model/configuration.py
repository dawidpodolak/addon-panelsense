from enum import Enum
from typing import List, Optional, Set, Union

from pydantic import BaseModel

from .base import *


class ConfigurationSystem(BaseModel):
    main_panel_id: Optional[str] = None
    show_nav_bar: bool = False
    background: Optional[str] = None


class ConfigurationItem(BaseModel):
    id: Optional[str] = None
    entity: str
    title: Optional[str] = None
    icon: Optional[str] = None
    background: Optional[str] = None

    def __hash__(self):
        return hash(self.id)


class ConfigurationPanelType(Enum):
    HOME = "home"
    GRID = "grid"


class ConfigurationPanel(BaseModel):
    id: Optional[str] = None
    type: str
    background: Optional[str] = None

    def __hash__(self):
        return hash(self.id)


class ConfigurationGridPanel(ConfigurationPanel):
    column_count: int = 1
    item_list: List[ConfigurationItem] = list()


class ConfigurationHomePanel(ConfigurationPanel):
    weather_entity: Optional[str] = None
    time24h: bool = False
    # deprecated
    item_left: Optional[ConfigurationItem] = None
    # deprecated
    item_right: Optional[ConfigurationItem] = None
    item_list: List[ConfigurationItem] = list()
    background: Optional[str] = None


ConfigurationPanelUnion = Union[ConfigurationGridPanel, ConfigurationHomePanel]


class Configuration(BaseModel):
    system: ConfigurationSystem
    panel_list: List[ConfigurationPanelUnion] = list()


class ConfigurationOutcomingMessage(ServerOutgoingMessage):
    type: MessageType = MessageType.CONFIGURATION
    data: Configuration


class ConfigurationError(Exception):
    message: str
