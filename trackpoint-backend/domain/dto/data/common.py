from pydantic import BaseModel


class ProjectEventStatDTO(BaseModel):
    """请求项目中事件统计信息的请求体"""
    project_id: str
    event_id: str
