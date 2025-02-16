from datetime import datetime
from pydantic import BaseModel
from domain.entity.client import Client
from utils import format_pydantic_datetime


class EventInfo(BaseModel):
    """事件id和名单条数据"""
    event_id: str
    event_name: str


class ProjectEventInfoVO(BaseModel):
    """用户所有项目id和项目名单条数据，用于查询上报记录时选择项目和事件"""
    project_id: str
    project_name: str
    events: list[EventInfo]


class QueryEventClientItemVO(BaseModel):
    """查询上报记录中的单个client"""
    id: str
    os: str
    os_version: str
    browser: str
    browser_version: str
    device: str | None
    lng: float
    lat: float

    @classmethod
    def from_entity(cls, c: Client):
        return cls(
            id=c.id,
            os=c.os,
            os_version=c.os_version,
            browser=c.browser,
            browser_version=c.browser_version,
            device=c.device,
            lng=c.lng,
            lat=c.lat
        )


class QueryRecordVO(BaseModel):
    """查询上报记录响应体"""
    id: str
    project_name: str
    event_name: str
    create_time: datetime
    client: QueryEventClientItemVO
    page_url: str
    params: dict

    class Config:
        json_encoders = {
            datetime: format_pydantic_datetime
        }

