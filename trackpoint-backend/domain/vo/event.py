from datetime import datetime
from pydantic import BaseModel, Field

from domain.bo.event import BindParamBO, ProjectOptionBO
from domain.bo.project import EventOptionBO
from enums import StatusEnum
from utils import format_pydantic_datetime


class EventOptionsVO(BaseModel):
    """用于创建/修改项目时选择默认/自定义事件"""
    default: list[EventOptionBO]
    custom: list[EventOptionBO]


class QueryEventVO(BaseModel):
    """查询事件列表响应体中的单个事件"""
    id: str
    name: str
    status: StatusEnum
    """事件状态"""
    description: str
    create_time: datetime | None
    update_time: datetime | None
    param_list: list[BindParamBO] = Field(description='绑定的参数列表')
    param_num: int = Field(description='该事件绑定的参数数量')
    project_list: list[ProjectOptionBO] = Field(description='所属项目列表')
    project_num: int = Field(description='该事件被几个正常的项目使用')

    class Config:
        # 自定义序列化配置
        json_encoders = {
            datetime: format_pydantic_datetime
        }
