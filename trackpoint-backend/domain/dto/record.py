from typing import Any
from pydantic import BaseModel, Field, field_validator

from domain.dto.common import OrderBy, PageQuery, TimePeriod
from exception import BusinessException
from utils import can_be_number


class FilterParamItem(BaseModel):
    """根据参数过滤上报记录"""
    name: str
    value: Any


class QueryRecordDTO(BaseModel):
    """查询上报记录请求体"""
    project_id: str = Field(
        description='项目id', alias='projectId')
    event_id: str = Field(
        description='事件id', alias='eventId')
    order_by: list[OrderBy] = Field(
        description='排序字段', default_factory=list, alias='orderBy')
    create_time_period: TimePeriod = Field(
        description='创建时间范围', default_factory=TimePeriod.default, alias='createTimePeriod')
    filter_param_list: list[FilterParamItem] = Field(
        description='过滤参数', default_factory=list, alias='filterParamList')
    page: PageQuery = Field(description='分页参数')

    @field_validator('order_by')
    def check_order_by(cls, ol: list[OrderBy]):
        """上报记录只支持按照创建时间排序"""
        return [o for o in ol if o.field == 'create_time' and o.order]

    @field_validator('filter_param_list')
    def check_filter_param_list(cls, ol: list[FilterParamItem]):
        """只要name不为空的参数"""
        return [o for o in ol if o.name]
