from typing import Any
from pydantic import BaseModel, Field

from domain.dto.common import TimePeriod



class IFilterEVentParam(BaseModel):
    """根据参数过滤记录"""
    name: str
    value: Any


class DataStat2DTO(BaseModel):
    """获取记录统计信息的请求体"""
    project_id: str
    event_id: str
    time_period: TimePeriod = Field(alias='timePeriod')
    time_granularity: str = Field(alias='timeGranularity', description='时间粒度')
    filter_param_list: list[IFilterEVentParam] = Field(
        alias='filterParamList', description='根据参数过滤')
