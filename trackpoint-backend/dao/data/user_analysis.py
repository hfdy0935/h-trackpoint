from fastapi_boot.core import Repository
from fastapi_boot.tortoise_util import Select

from domain.entity.record import Record
from domain.vo.data.user_analysis import UserVisitDataVO
from constants import DB_NAME_DICT


@Repository
class UserAnalysisDAO:
    @Select("""
        SELECT date(r.create_time) AS time, 
            COUNT(*) AS pv, 
            COUNT(DISTINCT client_id) AS uv
        FROM {record} r
        WHERE r.project_id = {pid}
        AND r.event_id = {eid}
        AND r.create_time BETWEEN {start} AND {end}
        GROUP BY date(r.create_time)
    """).fill_map(DB_NAME_DICT)
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
    """).fill_map(DB_NAME_DICT)
    async def get_click_data_record(
        self, pid: str, eid: str, page_url: str, width: int | float, height: int | float, start: str, end: str) -> list[Record]: ...
    """获取点击事件列表，只获取一定时间范围内，不按时间分组"""
