from pydantic import BaseModel, Field

from enums import StatusEnum


class EventOptionBO(BaseModel):
    """查询项目列表时里面的单个事件"""
    id: str
    name: str
    pid: str=Field(description='项目id')
    status:StatusEnum
