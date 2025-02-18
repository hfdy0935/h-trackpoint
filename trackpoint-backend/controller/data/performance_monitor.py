from typing import cast
from fastapi import Query
from fastapi_boot.core import Controller, Get, use_dep
from dependencies import use_login
from domain.entity.project import Project
from domain.entity.default_event import DefaultEvent
from exception import BusinessException
from domain.entity.event_project import EventProject
from domain.entity.record import Record
from domain.vo.common import BaseResp
from domain.vo.data.performance_monitor import PerformanceMonitorItemVO, PerformanceMonitorPerPageVO
from utils import calc_description_number


@Controller('/v1/data/performance-monitor', tags=['性能监控统计信息'])
class PerformanceMonitorController:
    user = use_dep(use_login)

    async def _ensure_owner(self, projectId: str):
        project = await Project.get_or_none(id=projectId, user_id=self.user.id)
        if project is None:
            raise BusinessException(detail='查询失败，项目不存在或无权限访问')
        de = await DefaultEvent.get_or_none(name='performance')
        if de is None:
            raise BusinessException(detail='查询失败，事件不存在')
        dp = await EventProject.filter(project_id=project.id, event_id=de.id)
        if len(dp) == 0:
            raise BusinessException(detail='查询失败，该项目未添加默认的"performance"事件')
        return de

    @Get(summary='获取性能监控统计信息')
    async def get(self, projectId: str = Query(description='项目id')):
        de = await self._ensure_owner(projectId)
        record_list = await Record.filter(project_id=projectId, event_id=de.id)
        params = [cast(dict, i.params) for i in record_list]
        dns, tcp, request, response, processing, load_event_duration, js_heap_size_used_percent = [
        ], [], [], [], [], [], []
        for p in params:
            dns.append(p['dns'])
            tcp.append(p['tcp'])
            request.append(p['request'])
            response.append(p['response'])
            processing.append(p['processing'])
            load_event_duration.append(p['load_event_duration'])
            js_heap_size_used_percent.append(p['js_heap_size_used_percent'])
        result = PerformanceMonitorItemVO(
            dns=calc_description_number(dns),
            tcp=calc_description_number(tcp),
            request=calc_description_number(request),
            response=calc_description_number(response),
            processing=calc_description_number(processing),
            load_event_duration=calc_description_number(load_event_duration),
            js_heap_size_used_percent=calc_description_number(
                [i/100 for i in js_heap_size_used_percent])
        )
        return BaseResp.ok(data=result)

    @Get('/per-page', summary='获取性能监控统计信息，按页面分组', response_model=BaseResp[list[PerformanceMonitorPerPageVO]])
    async def get_per_page(self, projectId: str = Query(description='项目id')):
        de = await self._ensure_owner(projectId)
        record_list = await Record.filter(project_id=projectId, event_id=de.id)
        dic: dict[str, list[Record]] = {}
        for r in record_list:
            dic.setdefault(r.page_url, []).append(r)
        result = []
        for page_url, record_list in dic.items():
            dns, tcp, request, response, processing, load_event_duration, js_heap_size_used_percent = [
            ], [], [], [], [], [], []
            params = [cast(dict, i.params) for i in record_list]
            for p in params:
                dns.append(p['dns'])
                tcp.append(p['tcp'])
                request.append(p['request'])
                response.append(p['response'])
                processing.append(p['processing'])
                load_event_duration.append(p['load_event_duration'])
                js_heap_size_used_percent.append(
                    p['js_heap_size_used_percent'])
            result.append(PerformanceMonitorPerPageVO(page_url=page_url, performance=PerformanceMonitorItemVO(
                dns=calc_description_number(dns),
                tcp=calc_description_number(tcp),
                request=calc_description_number(request),
                response=calc_description_number(response),
                processing=calc_description_number(processing),
                load_event_duration=calc_description_number(
                    load_event_duration),
                js_heap_size_used_percent=calc_description_number(
                    [i/100 for i in js_heap_size_used_percent])
            )))
        return BaseResp[list[PerformanceMonitorPerPageVO]].ok(data=result)
