from pydantic import BaseModel, Field
from datetime import datetime

from utils import format_pydantic_datetime


class RegisterVO(BaseModel):
    token: str


class LoginVO(RegisterVO):
    """登录响应体"""


class UserVO(BaseModel):
    """获取用户信息响应体"""
    id: str
    email: str
    nickname: str
    createTime: datetime
    projectNumLimit: int = Field(description='项目数量限制')
    eventNumLimit: int = Field(description='单个项目最大添加事件数量限制')
    projectNum:int=Field(description='用户当前项目数量')
    eventNum:int=Field(description='用户当前事件数量')

    
    class Config:
        json_encoders = {
            datetime: format_pydantic_datetime
        }


