from fastapi_boot.core import Repository
from fastapi_boot.tortoise_util import Select

from domain.entity.custom_event import CustomEvent
from domain.entity.default_event import DefaultEvent
from domain.entity.event_project import EventProject
from domain.entity.project import Project
from domain.entity.record import Record
from domain.vo.data.project_stat import ProjectStatVO
from domain.vo.data.user_analysis import UserVisitDataVO


@Repository
class UserAnalysisDAO:
    @Select("""
        select date(r.create_time) time, count(*) pv, count(distinct client_id) uv
             from {record} r where r.project_id={pid} and r.event_id={eid}
            and r.create_time between {start} and {end}
            group by date(r.create_time)
    """).fill(record=Record.Meta.table)
    async def get_user_visit_data(
        self, pid: str, eid: str, start: str, end: str) -> list[UserVisitDataVO]: ...
    """获取用户访问数据"""

    @Select("""
        SELECT * FROM {record} r
        WHERE r.project_id = {pid}
        AND r.event_id = {eid}
        AND r.create_time BETWEEN {start} AND {end}
        AND r.page_url = {page_url}
        AND JSON_UNQUOTE(JSON_EXTRACT(r.params, '$.w')) = {width}
        AND JSON_UNQUOTE(JSON_EXTRACT(r.params, '$.h')) = {height}
    """).fill(record=Record.Meta.table)
    async def get_click_data_record(
        self, pid: str, eid: str, page_url: str, width: int | float, height: int | float, start: str, end: str) -> list[Record]: ...
    """获取点击事件列表，只获取一定时间范围内，不按时间分组"""
