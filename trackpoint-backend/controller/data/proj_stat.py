from fastapi_boot.core import Controller, Get, use_dep

from dao.data.project_stat import DataDAO
from dependencies import use_login
from domain.vo.common import BaseResp

from domain.vo.data.project_stat import ProjectStatVO


@Controller('/v1/data/project-stat', tags=['项目数据统计'])
class DataController:
    user = use_dep(use_login)

    def __init__(self, data_dao: DataDAO) -> None:
        self.data_dao = data_dao

    @Get(summary='获取项目统计信息', response_model=BaseResp[list[ProjectStatVO]])
    async def get_project_stat(self):
        vo = await self.data_dao.getProjectEventStat(self.user.id)
        return BaseResp[list[ProjectStatVO]].ok(data=vo)
