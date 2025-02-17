from fastapi_boot.core import Service
from fastapi_boot.tortoise_util import Select

from domain.entity.event_project import EventProject
from domain.entity.project import Project
from domain.entity.record import Record
from domain.entity.user import User


@Service
class ResourceService:

    @Select("""
        select distinct u.* from {user} u, {record} r, {event_project} ep, {project} p
            where r.screen_shot_path={path} and r.event_id=ep.event_id and ep.project_id=p.id
""").fill(
        user=User.Meta.table,
        record=Record.Meta.table,
        event_project=EventProject.Meta.table,
        project=Project.Meta.table
    )
    async def get_owner_of_resource(self, path: str) -> User: ...
    # 获取资源的所有者
