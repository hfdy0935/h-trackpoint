from datetime import datetime
from pydantic import BaseModel, Field

from domain.bo.project import EventOptionBO
from enums import StatusEnum
from utils import format_pydantic_datetime


class CreateProjectVO(BaseModel):
    """创建项目响应体"""
    id: str
    key: str


class QueryProjectVO(BaseModel):
    """查询项目列表响应体中的单个项目"""
    id: str
    name: str
    status: StatusEnum
    """项目状态"""
    description: str
    create_time: datetime
    update_time: datetime
    event_list: list[EventOptionBO] = Field(description='该项目的事件列表')
    event_num: int = Field(description='该项目的事件数量')

    class Config:
        # 自定义序列化配置
        json_encoders = {
            datetime: format_pydantic_datetime
        }
