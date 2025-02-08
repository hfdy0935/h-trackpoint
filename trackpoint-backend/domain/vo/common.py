from pydantic import BaseModel, Field
from typing import Generic

from typing_extensions import TypeVar

from domain.dto.common import PageQuery


T = TypeVar('T')


class BaseResp(BaseModel, Generic[T]):
    code: int = 200
    msg: str = '请求成功'
    data: T | None = None

    @classmethod
    def ok(cls, code: int = 200, msg: str = '请求成功', data: T = None) -> 'BaseResp[T]':
        return cls(code=code, msg=msg, data=data)

    @classmethod
    def err(cls, code: int = 500, msg: str = '请求失败', data: T = None) -> 'BaseResp[T]':
        return cls(code=code, msg=msg, data=data)


class PageVO(BaseModel, Generic[T]):
    """分页查询结果"""
    page_num: int = Field(description='页码')
    page_size: int = Field(description='每页数量')
    total: int = Field(description='总数量')
    records: list[T] = Field(description='数据')

    @classmethod
    def create(cls, pq: PageQuery, total: int, records: list[T]):
        """从分页查询请求参数和查询结果构造，不执行分页，只组装结果"""
        return cls(
            **pq.model_dump(),
            total=total,
            records=records
        )
