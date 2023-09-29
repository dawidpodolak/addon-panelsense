from typing import Optional

from server.model.light import ServerMessage


class CoverModel(ServerMessage):
    entity_id: str
    position: Optional[int] = None
    state: str
