



from pydantic import BaseModel


class ProjectStatVO(BaseModel):
    """项目统计中响应体中的单个项目"""
    id: str
    name: str
    default_count: int
    """默认事件数量"""
    custom_count: int
    """自定义事件数量"""
    record_count: int
    """记录数量"""
    client_count: int
    """客户端数量"""
