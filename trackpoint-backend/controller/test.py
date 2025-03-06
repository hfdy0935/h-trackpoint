import asyncio
import random
from types import NoneType
from typing import Annotated
from fastapi import HTTPException, Query
from fastapi_boot.core import Controller,  Post, Get, use_dep

from domain.vo.common import BaseResp
from exception import BusinessException
from domain.entity.project import Project
from domain.entity.event_project import EventProject
from dependencies import use_login
from dao.event import CustomEventDAO
from domain.vo.event import QueryEventVO
from service.event import EventService


@Controller('/v1/test', tags=['调试'])
class TestController:
    """后台测试页面"""

    def __init__(self, ce_dao: CustomEventDAO, event_service: EventService) -> None:
        self.ce_dao = ce_dao
        self.event_service = event_service

    @Post('/random-result', summary='测试请求上报事件，结果随机', response_model=BaseResp[NoneType])
    async def test_request_send_event(self):
        i = random.randint(1, 3)
        await asyncio.sleep(i)
        if i == 1:
            raise HTTPException(status_code=500, detail='请求失败')
        elif i == 2:
            return BaseResp[NoneType].ok()
        else:
            raise BusinessException(detail='请求失败')

    @Get('/event-list', summary='获取自定义事件列表，用于调试自定义事件', response_model=BaseResp[list[QueryEventVO]])
    async def getEventListByPid(self, pid: Annotated[str, Query(description='项目id')], user=use_dep(use_login)):
        project = await Project.get_or_none(id=pid)
        if project is None:
            raise BusinessException(detail='获取失败，项目不存在')
        if project.user_id != user.id:
            raise BusinessException(detail='获取失败，无权限')
        eventList = await EventProject.filter(project_id=pid)
        if len(eventList) == 0:
            return BaseResp[list[QueryEventVO]].ok(data=[])
        data = await self.ce_dao.getDetailByEventIdList([e.event_id for e in eventList])
        return BaseResp[list[QueryEventVO]].ok(data=await self.event_service._combine_event_detail_result(data))
