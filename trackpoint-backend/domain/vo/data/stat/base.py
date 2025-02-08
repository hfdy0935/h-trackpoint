from pydantic import BaseModel, Field

from domain.entity.client import Client


class IClient(BaseModel):
    """单个客户端设备"""
    id: str
    os: str
    os_version: str
    browser: str
    browser_version: str
    device: str | None
    lng: float
    lat: float

    @classmethod
    def from_entity(cls, client: Client):
        """根据数据库实体类生成"""
        return cls(id=client.id, os=client.os,
                   os_version=client.os_version,
                   browser=client.browser,
                   browser_version=client.browser_version,
                   device=client.device,
                   lng=client.lng,
                   lat=client.lat
                   )


class BaseStatVO(BaseModel):
    """基本统计信息"""
    # project_num: str
    # event_num: str
    client_list: list[IClient] = Field(description='客户端列表')
