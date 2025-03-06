from fastapi_boot.core import Service
from fastapi_boot.tortoise_util import Select
from domain.entity.user import User
from constants import DB_NAME_DICT


@Service
class ResourceService:

    @Select("""
        SELECT DISTINCT u.*
        FROM {user} u
        JOIN {record} r ON r.event_id = ep.event_id
        JOIN {event_project} ep ON ep.project_id = p.id
        WHERE r.screen_shot_path = {path}
    """).fill_map(DB_NAME_DICT)
    async def get_owner_of_resource(self, path: str) -> User: ...
    # 获取资源的所有者
