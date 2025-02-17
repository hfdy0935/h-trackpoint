from pydantic import BaseModel, Field, field_validator

from domain.dto.common import OrderBy, PageQuery, TimePeriod
from enums import BindParamTypeEnum, EventTypeEnum, StatusEnum
from exception import BusinessException


class QueryEventDTO(BaseModel):
    """查询项目列表请求体"""
    type: EventTypeEnum = Field(
        description='事件类型，默认事件or自定义事件')
    project_id_list: list[str] | None = Field(
        description='所属项目id列表，[]表示不限制', default_factory=list, alias='projectIdList')
    keyword: str | None = Field(description='搜索关键词', default=None)
    status: list[StatusEnum] | None = Field(
        description='项目状态，None表示不做限制', default_factory=list)
    order_by: list[OrderBy] = Field(
        description='排序字段', default_factory=list, alias='orderBy')
    create_time_period: TimePeriod = Field(
        description='创建时间范围', default_factory=TimePeriod.default, alias='createTimePeriod')
    update_time_period: TimePeriod = Field(
        description='更新时间范围', default_factory=TimePeriod.default, alias='updateTimePeriod')
    page: PageQuery = Field(description='分页参数')

    def has_field_and_order(self, field: str):
        """排序参数中是否有指定字段，有就返回顺序"""
        for o in self.order_by:
            if o.field == field:
                return o.order

    @property
    def has_proj_num_and_order(self):
        return self.has_field_and_order('project_num')

    @property
    def has_param_num_and_order(self):
        return self.has_field_and_order('param_num')

    @field_validator('order_by')
    def check_order_by(cls, ol: list[OrderBy]):
        return [i for i in ol if i.field in ['create_time', 'update_time', 'project_num', 'param_num'] and i.order]


class UpdateEventStatusDTO(BaseModel):
    """修改事件状态请求体"""
    id: str
    status: StatusEnum


class EventParam(BaseModel):
    """创建事件请求体中的单个参数"""
    name: str
    description: str
    type: BindParamTypeEnum


class CreateEventDTO(BaseModel):
    """创建事件请求体"""
    name: str = Field(min_length=1)
    description: str
    param_list: list[EventParam] = Field(
        description='事件参数', default_factory=list, alias='paramList')
    project_id_list: list[str] = Field(
        description='事件要添加到哪些项目', default_factory=list, alias='projectIdList')

    @field_validator('param_list')
    def check_unique_names(cls, param_list: list[EventParam]):
        names = [param.name for param in param_list]
        if len(names) != len(set(names)):
            raise BusinessException(detail='参数名不能重复')
        return param_list


class UpdateEventDTO(CreateEventDTO, BaseModel):
    """修改事件请求体"""
    id: str = Field(description='事件id')
