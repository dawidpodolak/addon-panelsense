from typing import Optional

from server.model.server_message import ServerMessage


class CoverModel(ServerMessage):
    entity_id: str
    position: Optional[int] = None
    state: str
