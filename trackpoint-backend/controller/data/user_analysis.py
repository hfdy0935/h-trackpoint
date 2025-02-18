import os
from typing import cast
from fastapi import Query
from fastapi_boot.core import Controller, Get, use_dep, Post
from domain.entity.project import Project
from dependencies import use_login
from exception import BusinessException
from domain.entity.client import Client
from domain.vo.data.user_analysis import WH, XY, ClientVO, UserBehaviorAnalysisVO, UserClickDataVO, UserClickQueryInfoVO, UserStayDataVO
from domain.dto.data.user_behavior import UserBehaviorAnalysisDTO, UserClickDataDTO
from domain.vo.common import BaseResp
from domain.entity.record import Record
from domain.entity.event_project import EventProject
from domain.entity.default_event import DefaultEvent
from dao.data.user_analysis import UserAnalysisDAO
from domain.entity.custom_event import CustomEvent
from utils import calc_description_number
from constants import RESOURCE_PREFIX
from domain.config import ProjConfig
from domain.dto.common import TimePeriod


@Controller('/v1/data/user-analysis', tags=['用户分析接口'])
class UserAnalysisController:
    user = use_dep(use_login)

    def __init__(self, ua_dao: UserAnalysisDAO, cfg: ProjConfig) -> None:
        self.ua_dao = ua_dao
        self.server_url_prefix = cfg.server.deploy_address

    @Get('/distribution', summary='用户分布分析', response_model=BaseResp[list[ClientVO]])
    async def get_users(self, projectId: str = Query(description='项目id')):
        if not await Project.exists(id=projectId, user_id=self.user.id):
            raise BusinessException(detail='查询失败，项目不存在或无权限访问')
        record_list = await Record.filter(project_id=projectId)
        client_id_list = [r.client_id for r in record_list]
        client_list = await Client.filter(id__in=client_id_list)
        result = [
            ClientVO.from_entity(c) for c in client_list
        ]
        return BaseResp[list[ClientVO]].ok(data=result)

    def _adapt_time_period(self, tp: TimePeriod | None):
        start, end = '1900-01-01', '2200-01-01'
        if tp:
            if tp.start is not None:
                start = tp.start
            if tp.end is not None:
                end = tp.end
        return start, end

    @Post('/behavior', summary='用户行为分析', response_model=BaseResp[UserBehaviorAnalysisVO])
    async def get_user_behavior_analysis(self, dto: UserBehaviorAnalysisDTO):
        if not await Project.exists(id=dto.project_id, user_id=self.user.id):
            raise BusinessException(detail='查询失败，项目不存在或无权限访问')
        if not await DefaultEvent.exists(id=dto.event_id) and not await CustomEvent.exists(id=dto.event_id, user_id=self.user.id):
            raise BusinessException(detail='查询失败，事件不存在')
        if not await EventProject.exists(event_id=dto.event_id, project_id=dto.project_id):
            raise BusinessException(detail='查询失败，事件未绑定到项目中')
        start, end = self._adapt_time_period(dto.time_period)
        # 1. 用户访问量
        visit_data = await self.ua_dao.get_user_visit_data(dto.project_id, dto.event_id, start, end)
        # 2. 用户点击
        click_event_id = (await DefaultEvent.filter(name='click'))[0].id
        click_record_list = await Record.filter(project_id=dto.project_id, event_id=click_event_id, create_time__range=[start, end])
        # key是 url，value是dict[w_h, 1]
        click_dict: dict[str, dict[str, int]] = {}
        for r in click_record_list:
            p = cast(dict, r.params)
            w, h = p['w'], p['h']
            click_dict.setdefault(r.page_url, {}).setdefault(
                str(w)+'_'+str(h), 1)
        click_data = [UserClickQueryInfoVO(
            url=url,
            wh=[WH(w=int(wh.split('_')[0]), h=int(wh.split('_')[1])) for wh in wh_dict.keys()])
            for url, wh_dict in click_dict.items()]
        # 3. 用户停留时间
        stay_event_id = (await DefaultEvent.filter(name='page_stay_duration'))[0].id
        stay_reord_list = await Record.filter(project_id=dto.project_id, event_id=stay_event_id, create_time__range=[start, end])
        stay_dict: dict[str, list[int | float]] = {}
        for r in stay_reord_list:
            p = cast(dict, r.params)
            stay_dict.setdefault(r.page_url, []).append(
                p['time_duration'])
        stay_data = [
            UserStayDataVO(
                page_url=page_url,
                **calc_description_number(sl).model_dump()
            ) for page_url, sl in stay_dict.items()
        ]
        return BaseResp[UserBehaviorAnalysisVO].ok(data=UserBehaviorAnalysisVO(
            visit=visit_data,
            click=click_data,
            stay=stay_data
        ))

    @Post('/click-data', summary='获取点击数据详情', response_model=BaseResp[UserClickDataVO])
    async def get_click_data(self, dto: UserClickDataDTO):
        if not await Project.exists(id=dto.project_id, user_id=self.user.id):
            raise BusinessException(detail='查询失败，项目不存在或无权限访问')
        de = await DefaultEvent.get_or_none(name='click')
        if de is None:
            raise BusinessException(detail='查询失败，事件不存在')
        if not await EventProject.exists(event_id=de.id, project_id=dto.project_id):
            raise BusinessException(detail='查询失败，默认点击事件未绑定到项目中')
        start, end = self._adapt_time_period(dto.time_period)
        record_list = await self.ua_dao.get_click_data_record(dto.project_id,  de.id, dto.url, dto.width, dto.height, start, end)
        if len(record_list) == 0:
            return BaseResp[UserClickDataVO].ok(data=UserClickDataVO(
                url=dto.url,
                src='',
                wh=WH(w=dto.width, h=dto.height),
                xy=[]
            ))
        src = os.path.join(self.server_url_prefix,
                           RESOURCE_PREFIX, record_list[0].screen_shot_path)
        return BaseResp[UserClickDataVO].ok(
            data=UserClickDataVO(
                url=dto.url,
                src=src,
                wh=WH(w=dto.width, h=dto.height),
                xy=[XY(x=cast(dict, r.params)['x'], y=cast(dict, r.params)['y'])
                    for r in record_list]
            )
        )
