from pydantic import BaseModel

from domain.vo.data.common import DescriptionNumber


class PerformanceMonitorItemVO(BaseModel):
    """基本性能统计数据"""
    dns: DescriptionNumber
    tcp: DescriptionNumber
    request: DescriptionNumber
    response: DescriptionNumber
    processing: DescriptionNumber
    load_event_duration: DescriptionNumber
    js_heap_size_used_percent: DescriptionNumber


class PerformanceMonitorPerPageVO(BaseModel):
    """每个页面的性能指标"""
    page_url: str
    performance: PerformanceMonitorItemVO
