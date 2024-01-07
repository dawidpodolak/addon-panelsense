from enum import Enum
from typing import List, Optional, Set, Union

from pydantic import BaseModel

from .base import *


class ConfigurationSystem(BaseModel):
    main_panel_id: Optional[str] = None
    show_nav_bar: bool = False
    background: Optional[str] = None
    foreground: Optional[str] = None


class ConfigurationItem(BaseModel):
    id: Optional[str] = None
    entity: Optional[str] = None
<<<<<<< HEAD

    #  Supported type: CLOCK, GRID
=======
>>>>>>> master
    type: Optional[str] = None
    title: Optional[str] = None
    icon: Optional[str] = None
    background: Optional[str] = None
<<<<<<< HEAD
    foreground: Optional[str] = None

    # dedicated for clock type
    time24h: Optional[bool] = None

    # dedicated for sensor grid type
    item_list: Optional[List["ConfigurationItem"]] = None
=======
    time24h: Optional[bool] = None
>>>>>>> master

    def __hash__(self):
        return hash(self.id)


class ConfigurationPanelType(Enum):
    HOME = "home"
    GRID = "grid"
    FLEX = "flex"


class ConfigurationPanel(BaseModel):
    id: Optional[str] = None
    type: str
    background: Optional[str] = None
    foreground: Optional[str] = None

    def __hash__(self):
        return hash(self.id)


class ConfigurationGridPanel(ConfigurationPanel):
    column_count: int = 1
    item_list: List[ConfigurationItem] = list()
    background: Optional[str] = None
    foreground: Optional[str] = None


class ConfigurationHomePanel(ConfigurationPanel):
    weather_entity: Optional[str] = None
    time24h: bool = False
    item_list: List[ConfigurationItem] = list()
    background: Optional[str] = None
    foreground: Optional[str] = None


class ConfigurationFlexPanel(ConfigurationPanel):
    rows: Optional[List[List[ConfigurationItem]]] = None
    columns: Optional[List[List[ConfigurationItem]]] = None
    background: Optional[str] = None
<<<<<<< HEAD
    foreground: Optional[str] = None
=======
>>>>>>> master


ConfigurationPanelUnion = Union[
    ConfigurationGridPanel, ConfigurationHomePanel, ConfigurationFlexPanel
]


class Configuration(BaseModel):
    system: ConfigurationSystem
    panel_list: List[ConfigurationPanelUnion] = list()


class ConfigurationOutcomingMessage(ServerOutgoingMessage):
    type: MessageType = MessageType.CONFIGURATION
    data: Configuration


class ConfigurationError(Exception):
    message: str
