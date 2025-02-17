

from datetime import datetime
from pydantic import BaseModel
from enums import StatusEnum


class ProjectStatVO(BaseModel):
    """项目统计中响应体中的单个项目"""
    id: str
    name: str
    status: StatusEnum
    create_time:datetime
    default_count: int
    """默认事件数量"""
    custom_count: int
    """自定义事件数量"""
    record_count: int
    """记录数量"""
    client_count: int
    """客户端数量"""
    performance_total_time: float
    """所有默认performance事件的总时间的平均值，单位ms"""
    performance_js_rate: float
    """所有默认performance事件的js内存占比平均值，单位%"""
    request_error_rate: float
    """请求报错率，单位%"""
    js_error_count: int
    """js报错次数"""
