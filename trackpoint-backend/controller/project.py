from typing import Annotated
from fastapi import Path
from fastapi_boot.core import Controller, Post, Put, use_dep, Delete, Get

from constants import CacheConstant
from dependencies import use_login
from domain.bo.event import ProjectOptionBO
from domain.dto.project import CreateProjectDTO, QueryProjectDTO, UpdateProjectDTO, UpdateProjectStatusDTO
from domain.entity.custom_event import CustomEvent
from domain.entity.default_event import DefaultEvent
from domain.entity.project import Project
from domain.entity.record import Record
from domain.vo.common import BaseResp, PageVO
from domain.vo.project import CreateProjectVO, QueryProjectVO
from enums import StatusEnum
from exception import BusinessException
from helper import HBF
from service.project import ProjectService
from utils import gnow


@Controller('/v1/project', tags=['项目'])
class ProjectController:
    user = use_dep(use_login)

    def __init__(self, proj_service: ProjectService, bf: Annotated[HBF, CacheConstant.DEFAULT_EVENT_BF_NAME]) -> None:
        self.proj_service = proj_service
        # 布隆过滤器
        self.bf = bf

    @Get('/option', summary='获取用户的项目列表，用于创建/修改事件时选择', response_model=BaseResp[list[ProjectOptionBO]])
    async def get_project_options(self):
        data = [ProjectOptionBO(
            id=i.id,
            name=i.name,
            eid=i.id,
            status=i.status
        ) for i in await Project.filter(user_id=self.user.id)]
        return BaseResp.ok(data=data)

    @Get('/all', summary='获取所有项目信息，不全，用于创建或修改事件时选择项目')
    async def get_project_all(self):
        data = [ProjectOptionBO(
            id=i.id,
            name=i.name,
            eid='',
            status=i.status
        ) for i in await Project.filter(status=StatusEnum.NORMAL)]
        return BaseResp.ok(data=data)

    async def _ensure_owner(self, id: str) -> Project:
        """确保项目存在且属于当前用户

        Args:
            id (str): 项目id

        Returns:
            Project: 项目
        """
        # 目前不考虑状态，只要存在就能删除修改
        project = await Project.get_or_none(id=id)
        if project is None:
            raise BusinessException(detail='请求失败，项目不存在')
        if project.user_id != self.user.id:
            raise BusinessException(detail='请求失败，无权限')
        return project

    @Post(summary='创建项目', response_model=BaseResp[CreateProjectVO])
    async def create(self, dto: CreateProjectDTO):
        if len(dto.default_event_id_list)+len(dto.custom_event_id_list) > self.user.event_num_limit:
            raise BusinessException(detail='创建失败，事件数量超出限制')
        # 如果有自定义事件，确保都是当前用户的
        custom_event_list: list[CustomEvent] = []
        if dto.custom_event_id_list:
            custom_event_list = await CustomEvent.filter(id__in=dto.custom_event_id_list, user_id=self.user.id)
        if len(custom_event_list) != len(dto.custom_event_id_list):
            BusinessException(detail='请求失败，自定义事件不存在或无权限')
        res = await self.proj_service.create(self.user, dto, custom_event_list)
        return BaseResp.ok(msg='创建成功', data=res)

    @Delete('/{id}', summary='删除项目', response_model=BaseResp[None])
    async def delete(self, id: str = Path(description='项目id')):
        project = await self._ensure_owner(id)
        await self.proj_service.delete(project)
        # 删除该项目所有记录
        await Record.filter(project_id=project.id).delete()
        return BaseResp.ok(msg='删除成功')

    @Post('/list', summary='查询项目列表', response_model=BaseResp[PageVO[QueryProjectVO]])
    async def list(self, dto: QueryProjectDTO):
        data = await self.proj_service.list(self.user, dto)
        return BaseResp.ok(msg='获取成功', data=data)

    @Put(summary='修改项目', response_model=BaseResp[None])
    async def update_project(self, dto: UpdateProjectDTO):
        # 事件数量不能超过限制
        if len(dto.default_event_id_list)+len(dto.custom_event_id_list) > self.user.event_num_limit:
            raise BusinessException(detail='修改失败，事件数量超出限制')
        project = await self._ensure_owner(dto.id)
        # 如果传的默认事件id不存在
        deil = dto.default_event_id_list
        case1 = len(deil) > 1 and not self.bf.mexists(*deil)
        case2 = len(deil) == 1 and not self.bf.exists(deil[0])
        if case1 or case2:
            raise BusinessException(detail='修改失败，请确保默认事件都存在')
        de_list = await DefaultEvent.filter(id__in=dto.default_event_id_list)
        # 如果传的自定义事件id不存在或不属于当前用户
        ce_list = await CustomEvent.filter(user_id=self.user.id, id__in=dto.custom_event_id_list)
        if len(ce_list) != len(dto.custom_event_id_list):
            raise BusinessException(detail='修改失败，自定义事件不存在或无权限')
        # 事件名不能重复
        if set([i.name for i in de_list]) & set([i.name for i in ce_list]):
            raise BusinessException(detail='修改失败，事件名重复')
        await self.proj_service.update(project, dto)
        return BaseResp.ok(msg='修改成功')

    @Put('/status', summary='修改项目状态', response_model=BaseResp[None])
    async def update_status(self, dto: UpdateProjectStatusDTO):
        # 原来的状态
        project = await self._ensure_owner(dto.id)
        project.status = dto.status
        project.update_time = gnow()
        await project.save()
        return BaseResp.ok()
