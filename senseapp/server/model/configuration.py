from enum import Enum
from typing import List, Optional, Set

from pydantic import BaseModel

from .base import *


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


class Configuration(BaseModel):
    system: ConfigurationSystem
    panel_list: List[ConfigurationPanel] = list()


class ConfigurationOutcomingMessage(ServerOutgoingMessage):
    type: MessageType = MessageType.CONFIGURATION
    data: Configuration
