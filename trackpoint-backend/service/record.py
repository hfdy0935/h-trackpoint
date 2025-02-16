from typing import cast
from fastapi_boot.core import Service
from domain.dto.record import QueryRecordDTO
from domain.entity.record import Record
from domain.entity.client import Client
from domain.entity.project import Project
from domain.entity.custom_event import CustomEvent
from domain.entity.default_event import DefaultEvent
from domain.vo.record import QueryRecordVO, QueryEventClientItemVO
from domain.vo.common import PageVO
from utils import can_be_number


@Service
class RecordService:

    def resolve_default_event_performance_params(self, p: dict):
        """处理默认事件的性能参数，给时间添加ms，给js占用添加%"""
        for k, v in p.items():
            if k == 'js_heap_size_used_percent':
                p[k] = f'{p[k]} %'
            elif k in ['dns', 'tcp', 'request', 'response', 'processing', 'load_event_duration', 'time_duration']:
                p[k] = f'{p[k]} ms'
        return p

    async def query(self, dto: QueryRecordDTO, project: Project, event: DefaultEvent | CustomEvent) -> PageVO[QueryRecordVO]:
        """查询上报事件记录"""
        qs = Record.filter(project_id=dto.project_id, event_id=dto.event_id)
        # 时间范围
        if dto.create_time_period.start:
            qs = qs.filter(create_time__gte=dto.create_time_period.start)
        if dto.create_time_period.end:
            qs = qs.filter(create_time__lte=dto.create_time_period.end)
        # 排序
        for order in dto.order_by:
            if order.field and order.order:
                prefix = '' if order.order == 'ascend' else '-'
                qs = qs.order_by(prefix+order.field)
        # 过滤参数
        target_record_list: list[Record] = []
        for r in await qs:
            need_add = True
            for p in dto.filter_param_list:
                if str(cast(dict, r.params).get(p.name)) != str(p.value):
                    need_add = False
                    break
            if need_add:
                target_record_list.append(r)
        total_num = len(target_record_list)
        # 分页
        page_result = dto.page.execute(target_record_list)
        # client dict
        client_dict = {i.id: i for i in await Client.filter(id__in=[i.client_id for i in page_result])}
        # 组装结果
        result: list[QueryRecordVO] = []
        for p in page_result:
            params = self.resolve_default_event_performance_params(cast(
                dict, p.params)) if isinstance(event, DefaultEvent) else cast(dict, p.params)
            result.append(QueryRecordVO(
                id=p.id,
                project_name=project.name,
                event_name=event.name,
                create_time=p.create_time,
                client=QueryEventClientItemVO.from_entity(
                    client_dict[p.client_id]),
                page_url=p.page_url,
                params=params))
        return PageVO[QueryRecordVO].create(dto.page, total_num, result)
