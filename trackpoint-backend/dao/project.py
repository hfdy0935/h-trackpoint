from fastapi_boot.core import Repository
from fastapi_boot.tortoise_util import Select

from domain.bo.event import ProjectOptionBO
from domain.entity.project import Project
from constants import DB_NAME_DICT


@Repository
class ProjectDAO:

    @Select("""
        SELECT p.id, p.name, p.status, ep.event_id AS eid
        FROM {event_project} ep
        JOIN {project} p ON ep.project_id = p.id
        WHERE ep.event_id IN {eid_list}
    """).fill_map(DB_NAME_DICT)
    async def getProjectBvEventIdList(
        self, eid_list: list[str]) -> list[ProjectOptionBO]: ...
    # 根据事件id获取事件所在项目的简略信息列表

    @Select("""
        SELECT p.*
        FROM {event_project} ep
        JOIN {project} p ON ep.project_id = p.id
        WHERE ep.event_id = {eid}
    """).fill_map(DB_NAME_DICT)
    async def get_by_event_id(self, eid: str) -> list[Project]: ...
    # 根据自定义事件id获取项目
