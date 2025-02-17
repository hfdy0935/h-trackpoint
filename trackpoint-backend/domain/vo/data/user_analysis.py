from collections import namedtuple
from datetime import datetime
from pydantic import BaseModel
from domain.entity.client import Client


class ClientVO(BaseModel):
    """单个客户端设备"""
    id: str
    os: str
    os_version: str
    browser: str
    browser_version: str
    device: str | None = ''
    lng: float
    lat: float

    @classmethod
    def from_entity(cls, c: Client):
        return cls(
            id=c.id,
            os=c.os,
            os_version=c.os_version,
            browser=c.browser,
            browser_version=c.browser_version,
            device=c.device,
            lng=c.lng,
            lat=c.lat,
        )

# ---------------------------------- 用户行为分析 ---------------------------------- #


class UserVisitDataVO(BaseModel):
    """用户访问量pv、uv统计"""
    time: str | datetime
    pv: int
    uv: int

    class Config:
        json_encoders = {
            datetime: lambda d: d.strftime('%Y-%m-%d')
        }


WH = namedtuple('wh', ['w', 'h'])


class UserClickQueryInfoVO(BaseModel):
    """用户点击量统计"""
    url: str
    wh: list[WH]


class UserStayDataVO(BaseModel):
    """用户页面停留时长统计"""
    page_url: str
    max: int | float
    avg: int | float
    min: int | float


class UserBehaviorAnalysisVO(BaseModel):
    """分析用户行为响应体"""
    visit: list[UserVisitDataVO]
    click: list[UserClickQueryInfoVO]
    stay: list[UserStayDataVO]


# --------------------------------- 获取点击数据详情 --------------------------------- #
XY = namedtuple('xy', ['x', 'y'])


class UserClickDataVO(BaseModel):
    url: str
    """页面url，哪个页面的截图"""
    src: str
    """截图url"""
    wh: WH
    xy: list[XY]
