from datetime import datetime
from typing import List
from pydantic import BaseModel
from pydantic import Field

from enums import ClientDeviceEnum


class IOS(BaseModel):
    name: str = Field(description='名', default='')
    version: str = Field(description='版本', default='')


class Browser(IOS):
    ...


class ClientRegisterDTO(BaseModel):
    """客户端注册时的请求体"""
    project_id: str = Field(alias='projectId', description='项目id')
    key: str = Field(description='项目key')
    client_id: str = Field(min_length=36, max_length=36, alias='uid',
                           description='前端生成的uid')
    os: IOS = Field(description='操作系统')
    device: ClientDeviceEnum | None = Field(
        description='设备类型，和ua-parser-js的保持一致，可为空', default=None)
    browser: Browser = Field(description='浏览器')


# class ClientSendEventDTO(BaseModel):
#     """客户端上报事件的请求体"""
#     client_id: str = Field(description='客户端id', alias='uid')
#     project_id: str = Field(alias='projectId', description='项目id')
#     key: str = Field(description='项目key')
#     event_name:  str = Field(description='事件名，同一个项目唯一', alias='eventName')
#     params: dict = Field(description='额外参数，需要和该事件的配置进行校验，确保数据库中有的都有',
#                          default_factory=dict)
#     page_url: str = Field(description='页面url', default='', alias='pageUrl')
#     create_time: datetime = Field(
#         description='上报时间', alias='createTime')

class EventDTO(BaseModel):
    """事件对象"""
    event_name: str = Field(description='事件名')
    params: dict = Field(description='事件的额外参数', default_factory=dict)
    page_url: str = Field(description='页面url', default='')
    create_time: datetime = Field(description='上报时间')

class ClientSendEventsDTO(BaseModel):
    """客户端上报事件的请求体"""
    client_id: str = Field(description='客户端id', alias='uid')
    project_id: str = Field(alias='projectId', description='项目id')
    key: str = Field(description='项目key')
    events: List[EventDTO] = Field(description='事件列表')