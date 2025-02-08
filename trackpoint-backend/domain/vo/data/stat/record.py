from datetime import datetime
from pydantic import BaseModel, Field


class IRecord(BaseModel):
    """记录统计中的单个事件记录"""
    id: str
    project_id: str
    send_time: datetime = Field(description='发送时间')
    page_url: str
    params: dict = Field(description='参数')


class DataStat2VO(BaseModel):
    """获取记录统计信息响应体"""
    project_id: str
    event_id: str
    record_list: list[IRecord] = Field(description='记录列表')
