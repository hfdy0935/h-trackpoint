from types import NoneType
from fastapi_boot.core import Controller, Get, use_dep, Post, Put, Delete
from fastapi import Path

from dependencies import use_login
from domain.dto.record import QueryRecordDTO
from domain.entity.custom_event import CustomEvent
from domain.entity.default_event import DefaultEvent
from domain.entity.event_project import EventProject
from domain.entity.project import Project
from domain.entity.record import Record
from domain.vo.common import BaseResp, PageVO
from exception import BusinessException
from service.record import RecordService
from domain.vo.record import EventInfo, ProjectEventInfoVO, QueryRecordVO
from dao.event import DefaultEventDAO, CustomEventDAO


@Controller('/v1/record', tags=['上报记录'])
class RecordController:
    user = use_dep(use_login)

    def __init__(self, record_service: RecordService, de_dao: DefaultEventDAO, ce_dao: CustomEventDAO) -> None:
        self.record_service = record_service
        self.de_dao = de_dao
        self.ce_dao = ce_dao

    @Get('/proj-event-detail', summary='获取用户各项目下的事件，用于筛选上报记录', response_model=BaseResp[list[ProjectEventInfoVO]])
    async def get_project_event_info(self):
        result: list[ProjectEventInfoVO] = []
        project_list = await Project.filter(user_id=self.user.id)
        for p in project_list:
            item = (await self.de_dao.getByProjIdList([p.id]))+(await self.ce_dao.getByProjIdList([p.id]))
            result.append(ProjectEventInfoVO(
                project_id=p.id,
                project_name=p.name,
                events=[EventInfo(event_id=i.id, event_name=i.name)
                        for i in item]
            ))
        return BaseResp[list[ProjectEventInfoVO]].ok(data=result)

    @Post('/list', summary='查询事记录列表', response_model=BaseResp[PageVO[QueryRecordVO]])
    async def query(self, dto: QueryRecordDTO):
        # project, event = await self._ensure_owner(dto.project_id, dto.event_id)
        project = await Project.get_or_none(id=dto.project_id)
        if project is None or project.user_id != self.user.id:
            return BaseResp.ok(data=PageVO.create(dto.page, 0, []))
        event_project = await EventProject.get_or_none(event_id=dto.event_id, project_id=dto.project_id)
        if event_project is None:
            return BaseResp.ok(data=PageVO.create(dto.page, 0, []))
        event = await DefaultEvent.get_or_none(id=dto.event_id) or await CustomEvent.get_or_none(id=dto.event_id)
        if event is None:
            return BaseResp.ok(data=PageVO.create(dto.page, 0, []))
        result = await self.record_service.query(dto, project, event)
        return BaseResp[PageVO[QueryRecordVO]].ok(data=result)

    @Delete('/{id}', summary='删除上报记录', response_model=BaseResp[NoneType])
    async def delete(self, id: str = Path(description='上报记录id')):
        record = await Record.get_or_none(id=id)
        if record is None:
            raise BusinessException(detail='删除失败，记录不存在')
        project = await Project.get_or_none(id=record.project_id)
        if project is None:
            raise BusinessException(detail='删除失败，项目不存在')
        if project.user_id != self.user.id:
            raise BusinessException(detail='删除失败，无权限')
        await record.delete()
        return BaseResp.ok(msg='删除成功')
