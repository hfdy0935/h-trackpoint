from datetime import datetime
from pydantic import BaseModel, Field


class EventStatVO(BaseModel):
    """事件统计中的单个事件"""
    id: str
    name: str
    count: int
    """项目数量"""
