from typing import Generic, Literal, TypeVar, overload
from pydantic import BaseModel, Field
from tortoise.queryset import QuerySet
from tortoise.models import Model

from constants import FORMAT_DATETIME_PATTERN


T = TypeVar('T', bound=Model)


class PageQuery(BaseModel):
    """分页查询"""
    page_num: int = Field(description='页码', alias='pageNum')
    page_size: int = Field(description='每页数量', alias='pageSize')

    @overload
    def execute(self, q: QuerySet[T]) -> QuerySet[T]: ...

    @overload
    def execute(self, q: list[T]) -> list[T]: ...

    def execute(self, q: QuerySet[T] | list[T]) -> QuerySet[T] | list[T]:
        start = (self.page_num-1)*self.page_size
        if isinstance(q, QuerySet):
            return q.offset(start).limit(self.page_size)
        else:
            return q[start:start+self.page_size]


class OrderBy(BaseModel):
    """查询时字段排序"""
    field: str | None = None
    order: Literal['ascend', 'descend', None] = None


class TimePeriod(BaseModel):
    """查询时时间范围，如果是N则无限制"""
    start: str | None = Field(
        description='开始时间', default=None, pattern=FORMAT_DATETIME_PATTERN)
    end: str | None = Field(description='结束时间', default=None,
                            pattern=FORMAT_DATETIME_PATTERN)

    @classmethod
    def default(cls):
        return cls(start=None, end=None)
