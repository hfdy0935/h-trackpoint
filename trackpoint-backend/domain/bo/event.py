from datetime import datetime
from pydantic import BaseModel, Field
from enums import BindParamTypeEnum, StatusEnum



class BindParamBO(BaseModel):
    """
    用户事件绑定的单个参数
    """
    id: str
    name: str
    description: str
    type: BindParamTypeEnum
    """参数类型"""
    eid: str
    """事件id"""


class ProjectOptionBO(BaseModel):
    """单个项目选项"""
    id: str
    name: str
    eid: str = Field(description='事件id')
    status: StatusEnum


class QueryEventDetailBO(BaseModel):
    """查询事件详情时数据库返回的单个事件"""
    id: str
    name: str
    description: str
    status: StatusEnum
    create_time: datetime | None = None
    update_time: datetime | None = None
    bpid_list: list | str | None = Field(
        description='该事件绑定的参数id列表，用逗号分隔，如果没有参数返回None')
    pid_list: list | str | None = Field(
        description='该事件所属的项目id列表，用逗号分隔，如果没有项目返回None')
    project_num: int = Field(description='该事件所属的项目数量')
    param_num: int = Field(description='该事件绑定的参数数量')

    def format(self):
        """把bpid_list和pid_list转换为列表"""
        if type(self.bpid_list) is str:
            self.bpid_list = self.bpid_list.split(',')
        elif self.bpid_list is None:
            self.bpid_list = []
        if type(self.pid_list) is str:
            self.pid_list = self.pid_list.split(',')
        elif self.pid_list is None:
            self.pid_list = []
        return self


class QueryEventNameByProjectIdListBO(BaseModel):
    """根据项目id列表查询包含的事件名称列表"""
    name: str


