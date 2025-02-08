from fastapi_boot.core import Repository
from fastapi_boot.tortoise_util import Select

from domain.bo.event import ProjectOptionBO
from domain.entity.custom_event import CustomEvent
from domain.entity.event_project import EventProject
from domain.entity.project import Project
from enums import StatusEnum


@Repository
class ProjectDAO:

    @Select("""
        select p.id, p.name, p.status, ep.event_id eid from {event_project} ep, {project} p
            where ep.event_id in {eid_list} and ep.project_id=p.id
    """).fill(event_project=EventProject.Meta.table, project=Project.Meta.table)
    async def getProjectBvEventIdList(
        self, eid_list: list[str]) -> list[ProjectOptionBO]: ...
    # 根据事件id获取事件所在项目的简略信息列表

    @Select("""
        select p.* from {event_project} ep, {project} p
            where ep.event_id={eid} and ep.project_id=p.id
    """).fill(event_project=EventProject.Meta.table, project=Project.Meta.table)
    async def get_by_event_id(self, eid: str) -> list[Project]: ...
    # 根据自定义事件id获取项目
