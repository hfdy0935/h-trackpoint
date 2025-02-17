from pydantic import BaseModel, Field, field_validator

from domain.dto.common import OrderBy, PageQuery, TimePeriod
from enums import StatusEnum


class CreateProjectDTO(BaseModel):
    """创建项目请求体"""
    name: str = Field(description='项目名，不能为空', min_length=1, max_length=20)
    description: str = Field(description='项目描述，可以为空',
                             default='', max_length=300)
    default_event_id_list: list[str] = Field(
        description='默认事件id列表', default_factory=list, alias='defaultEventIdList')
    custom_event_id_list: list[str] = Field(
        description='自定义事件id列表', default_factory=list, alias='customEventIdList')


class QueryProjectDTO(BaseModel):
    """查询项目列表请求体"""
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

    @field_validator('order_by')
    def check_order_by(cls, ol: list[OrderBy]):
        return [i for i in ol if i.field in ['create_time', 'update_time', 'event_num'] and i.order]

    def has_field_and_order(self, field: str):
        """排序参数中是否有指定字段，有就返回顺序"""
        for o in self.order_by:
            if o.field == field:
                return o.order

    @property
    def has_event_num_and_order(self):
        return self.has_field_and_order('event_num')


class UpdateProjectDTO(BaseModel):
    """更新项目请求体"""
    id: str = Field(description='项目id')
    name: str | None = Field(description='项目名称', min_length=1, max_length=20)
    description: str | None = Field(
        description='项目描述', default=None, max_length=300)
    status: list[StatusEnum] | None = Field(
        description='项目状态', default=None)
    default_event_id_list: list[str] = Field(
        description='默认事件id列表', default_factory=list, alias='defaultEventIdList')
    custom_event_id_list: list[str] = Field(
        description='自定义事件id列表', default_factory=list, alias='customEventIdList')


class UpdateProjectStatusDTO(BaseModel):
    """修改项目状态请求体"""
    id: str
    status: StatusEnum
