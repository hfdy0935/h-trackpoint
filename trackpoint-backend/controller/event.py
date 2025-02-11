from fastapi_boot.core import Controller, Get, use_dep, Post, Put, Delete
from fastapi import Path

from dao.event import CustomEventDAO, DefaultEventDAO
from dao.project import ProjectDAO
from dependencies import use_login
from domain.bo.project import EventOptionBO
from domain.dto.event import CreateEventDTO, QueryEventDTO, UpdateEventDTO, UpdateEventStatusDTO
from domain.entity.custom_event import CustomEvent
from domain.entity.default_event import DefaultEvent
from domain.entity.event_project import EventProject
from domain.entity.project import Project
from domain.entity.record import Record
from domain.vo.common import BaseResp
from domain.vo.event import EventOptionsVO
from enums import StatusEnum
from exception import BusinessException
from service.event import EventService
from utils import gnow


@Controller('/v1/event', tags=['事件'])
class EventController:
    user = use_dep(use_login)

    def __init__(self, event_service: EventService, de_dao: DefaultEventDAO, ce_dao: CustomEventDAO, proj_dao: ProjectDAO) -> None:
        self.event_service = event_service
        self.de_dao = de_dao
        self.ce_dao = ce_dao
        self.proj_dao = proj_dao

    @Post(summary='创建事件', response_model=BaseResp[None])
    async def create(self, dto: CreateEventDTO):
        # 确保要添加的项目都存在且是当前用户自己的
        proj_list = await Project.filter(id__in=dto.project_id_list, user_id=self.user.id)
        if len(proj_list) != len(dto.project_id_list):
            raise BusinessException(detail='创建失败，有项目不存在或无权限')
        # 确保新建的事件名不和项目中原有事件名重复
        if dto.project_id_list:
            event_name_list_in_proj_list = [
                *(i.name for i in await self.de_dao.getEventNameListByProjIdList(dto.project_id_list)),
                *(i.name for i in await self.ce_dao.getEventNameListByProjIdList(dto.project_id_list))
            ]
            if dto.name in event_name_list_in_proj_list:
                raise BusinessException(detail='创建失败，事件名和已选项目中的事件名重复')
        # 要添加的每个项目的事件数量限制
        for pid in dto.project_id_list:
            event_num = await EventProject.filter(project_id=pid).count()
            if event_num+1 >= self.user.event_num_limit:
                raise BusinessException(detail='添加失败，项目事件数量已达上限')
        await self.event_service.create(dto, self.user, proj_list)
        return BaseResp.ok(msg='创建成功')

    @Put(summary='修改事件')
    async def update_event(self, dto: UpdateEventDTO):
        # 暂定不能修改默认事件
        if await DefaultEvent.exists(id=dto.id):
            raise BusinessException(detail='修改失败，无权限')
        # 确保事件存在且是当前用户自己的
        event = await self._ensure_owner(dto.id)
        if dto.project_id_list:
            # 传的项目id列表都存在且属于当前用户
            total_proj_list = await Project.filter(user_id=self.user.id)
            total_proj_id_list = [i.id for i in total_proj_list]  # 用户所有项目id列表
            if not set(dto.project_id_list).issubset(set(total_proj_id_list)):
                raise BusinessException(detail='修改失败，项目不存在或无权限')
            # 该事件原来添加的的项目
            event_proj_id_list = [i.id for i in await self.proj_dao.get_by_event_id(dto.id)]
            for pid in dto.project_id_list:
                # 如没改名，且原来有该项目
                if dto.name == event.name and pid in event_proj_id_list:
                    continue
                event_name_list = [
                    *(i.name for i in await self.de_dao.getEventNameListByProjIdList([pid])),
                    *(i.name for i in await self.ce_dao.getEventNameListByProjIdList([pid]))
                ]
                if pid not in event_proj_id_list and len(dto.project_id_list) > self.user.event_num_limit:
                    raise BusinessException(detail='修改失败，有项目的事件数量已达上限')
                if dto.name in event_name_list:
                    raise BusinessException(detail='修改失败，事件名和已选项目中的事件名重复')
            project_list = [
                i for i in total_proj_list if i.id in dto.project_id_list]
        else:
            project_list = []
        await self.event_service.update(dto, event, project_list)
        return BaseResp.ok(msg='修改成功')

    @Get('/option', summary='获取事件选项，用于创建/修改项目时选择', response_model=BaseResp[EventOptionsVO])
    async def get_event_options(self):
        default = [
            EventOptionBO(id=i.id, name=i.name, pid='', status=i.status) for i in await DefaultEvent.filter(status=StatusEnum.NORMAL)
        ]
        custom = [
            EventOptionBO(id=i.id, name=i.name, pid='', status=i.status) for i in await CustomEvent.filter(user_id=self.user.id)
        ]
        data = EventOptionsVO(default=default, custom=custom)
        return BaseResp.ok(data=data)

    @Post('/list', summary='查询事件列表')
    async def query(self, dto: QueryEventDTO):
        # 如果传了查询的项目，确保这些项目都是当前用户的
        if dto.project_id_list:
            proj_list = await Project.filter(id__in=dto.project_id_list, user_id=self.user.id)
            if len(proj_list) != len(dto.project_id_list):
                raise BusinessException(detail='查询失败，查询的项目不存在或无权限')
        return BaseResp.ok(data=await self.event_service.query(dto))

    async def _ensure_owner(self, eid: str):
        """确保事件存在、是自定义事件且是当前用户的"""
        event = await CustomEvent.get_or_none(id=eid)
        if event is None:
            raise BusinessException(detail='修改失败，事件不存在')
        if event.user_id != self.user.id:
            raise BusinessException(detail='修改失败，没有权限')
        return event

    @Put('/status', summary='修改事件状态', response_model=BaseResp[None])
    async def update_status(self, dto: UpdateEventStatusDTO):
        if await DefaultEvent.exists(id=dto.id):
            # TODO 判断是不是管理员，或者管理员重新写个接口
            raise BusinessException(detail='修改失败，默认事件无权限修改')
        # 原来的状态
        event = await self._ensure_owner(dto.id)
        event.status = dto.status
        event.update_time = gnow()
        await event.save()
        return BaseResp.ok()

    @Delete('/{id}', summary='删除事件', response_model=BaseResp[None])
    async def delete(self, id: str = Path(description='项目id')):
        if await DefaultEvent.get_or_none(id=id):
            await EventProject.filter(event_id=id).delete()
            # 删除该事件所有的记录
            await Record.filter(event_id=id).delete()
            return BaseResp.ok(msg='删除成功')
        elif event := await CustomEvent.get_or_none(id=id):
            if event.user_id != self.user.id:
                raise BusinessException(detail='删除失败，没有权限')
            await EventProject.filter(event_id=event.id).delete()  # 删除事件项目记录
            await event.delete()  # 删除自定义事件
            return BaseResp.ok(msg='删除成功')
        else:
            raise BusinessException(detail='删除失败，事件不存在')
