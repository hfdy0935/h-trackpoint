from pydantic import BaseModel
from domain.dto.client import ClientSendEventsDTO


class IEvent(BaseModel):
    id: str
    need_shot: bool


class ClientSendEventBO(BaseModel):
    """上报事件，Controller给Service传的"""
    dto: ClientSendEventsDTO
    db_event_dict: dict[str, IEvent]
    client_id: str
    screen_shot_path: str
