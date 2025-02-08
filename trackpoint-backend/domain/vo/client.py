from pydantic import BaseModel
from pydantic import Field


class CLientRegisterVO(BaseModel):
    """客户端注册响应体"""


class SendEventVO(BaseModel):
    """上报事件响应体"""
    record_id: str = Field(description='记录id')
    need_upload_shot: bool = Field(description='是否需要上传document.body截图')
