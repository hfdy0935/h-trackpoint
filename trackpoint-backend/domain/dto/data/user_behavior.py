from pydantic import BaseModel, Field
from domain.dto.common import TimePeriod


class UserBehaviorAnalysisDTO(BaseModel):
    """分析用户行为请求体"""
    project_id: str = Field(alias="projectId")
    event_id: str = Field(alias="eventId")
    time_period: TimePeriod | None = Field(alias="timePeriod", default=None)


class UserClickDataDTO(UserBehaviorAnalysisDTO, BaseModel):
    """用户点击数据详情请求体"""
    url: str
    width: int
    height: int
