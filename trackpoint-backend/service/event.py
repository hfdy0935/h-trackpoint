from typing import Literal
from fastapi_boot.core import Service
from tortoise.expressions import Q
from tortoise.transactions import atomic

from dao.event import DefaultEventDAO, CustomEventDAO, EventDAO
from dao.project import ProjectDAO
from domain.bo.event import QueryEventDetailBO
from domain.dto.event import CreateEventDTO, QueryEventDTO, UpdateEventDTO
from domain.entity.bind_param import BindParam
from domain.entity.default_event import DefaultEvent
from domain.entity.event_project import EventProject
from domain.entity.custom_event import CustomEvent
from domain.entity.eventbind_param import EventBindParam
from domain.entity.project import Project
from domain.entity.user import User
from domain.vo.common import PageVO
from domain.vo.event import QueryEventVO
from enums import EventTypeEnum, StatusEnum
from utils import gid, gnow


@Service
class EventService:
    def __init__(self, de_dao: DefaultEventDAO, ce_dao: CustomEventDAO, e_dao: EventDAO, p_dao: ProjectDAO) -> None:
        self.de_dao = de_dao
        self.ce_dao = ce_dao
        self.e_dao = e_dao
        self.p_dao = p_dao

    async def __combine_event_detail_result(self, event_list: list[QueryEventDetailBO]):
        """根据事件列表组装结果，包括默认事件和自定义事件"""
        id_list = [i.id for i in event_list]
        # 每个事件所属的项目信息列表，包括停用的项目
        p_list = await self.p_dao.getProjectBvEventIdList(id_list) if event_list else []
        # 每个事件的绑定参数列表
        bp_list = await self.e_dao.getBindParamListByEventIdList(id_list) if event_list else []
        # 组装结果
        records: list[QueryEventVO] = []
        for de in event_list:
            de.format()
            p_list_ = list(filter(lambda x: x.eid == de.id, p_list))
            bp_list_ = list(filter(lambda x: x.eid == de.id, bp_list))
            records.append(QueryEventVO(
                id=de.id, name=de.name, status=de.status, description=de.description, create_time=de.create_time,
                update_time=de.update_time, param_list=bp_list_, project_list=p_list_, project_num=de.project_num,
                param_num=de.param_num
            ))
        return records

    async def _query_default_event_list(self, event_id_list: list[str], dto: QueryEventDTO) -> list[QueryEventVO]:
        """查询用户的默认事件详情"""
        # 关键词
        qs = DefaultEvent.filter(id__in=event_id_list)
        if dto.keyword:
            qs = qs.filter(Q(name__icontains=dto.keyword) | Q(
                description__icontains=dto.keyword))
        # 状态
        if dto.status:
            qs = qs.filter(status__in=dto.status)
        # 分页
        qs = dto.page.execute(qs)
        # 筛选后的默认事件id列表
        event_id_list = [i.id for i in await qs]
        if len(event_id_list) == 0:
            return []
        de_list: list[QueryEventDetailBO] = await self.de_dao.getDetailByEventIdList(event_id_list)
        return await self.__combine_event_detail_result(de_list)

    async def _query_custom_event_list(self, event_id_list: list[str], dto: QueryEventDTO) -> list[QueryEventVO]:
        """查询用户的自定义事件详情"""
        qs = CustomEvent.filter(id__in=event_id_list)
        # 关键词
        if dto.keyword:
            qs = qs.filter(Q(name__icontains=dto.keyword) | Q(
                description__icontains=dto.keyword))
        # 状态
        if dto.status:
            qs = qs.filter(status__in=dto.status)
        # 分页
        qs = dto.page.execute(qs)
        # 排序
        for order in dto.order_by:
            if order.field and order.order and order.field not in ['project_num', 'param_num']:
                prefix = '' if order.order == 'ascend' else '-'
                qs = qs.order_by(prefix+order.field)
        # 时间
        if dto.create_time_period.start:
            qs = qs.filter(create_time__gte=dto.create_time_period.start)
        if dto.create_time_period.end:
            qs = qs.filter(create_time__lte=dto.create_time_period.end)
        if dto.update_time_period.start:
            qs = qs.filter(update_time__gte=dto.update_time_period.start)
        if dto.update_time_period.end:
            qs = qs.filter(update_time__lte=dto.update_time_period.end)
        # 筛选后的自定义事件id列表
        event_id_list = [i.id for i in await qs]
        if len(event_id_list) == 0:
            return []
        ce_list: list[QueryEventDetailBO] = await self.ce_dao.getDetailByEventIdList(event_id_list)
        # 如果传了项目列表，就不查项目数量为0的事件
        if dto.project_id_list:
            ce_list = [i for i in ce_list if i.project_num > 0]
        return await self.__combine_event_detail_result(ce_list)

    async def query(self, dto: QueryEventDTO) -> PageVO[QueryEventVO]:
        # 1. 已添加到项目的事件
        qs = EventProject.all()
        # 指定项目中的事件
        if dto.project_id_list:
            qs = qs.filter(project_id__in=dto.project_id_list)
        event_id_list = [i.event_id for i in await qs]
        # 没筛选项目的时候带上未添加到任何项目的自定义事件
        if not dto.project_id_list:
            event_id_list.extend([i.id for i in await CustomEvent.filter(id__not_in=event_id_list)])
        data: list[QueryEventVO] = []
        if len(event_id_list) > 0:
            if dto.type == EventTypeEnum.DEFAULT:
                data = await self._query_default_event_list(event_id_list, dto)
            else:
                data = await self._query_custom_event_list(event_id_list, dto)
            # 如果需要按照项目数量排序
            if o := dto.has_proj_num_and_order:
                data.sort(key=lambda x: x.project_num, reverse=o == 'descend')
            elif o := dto.has_param_num_and_order:
                data.sort(key=lambda x: x.param_num, reverse=o == 'descend')
        return PageVO[QueryEventVO].create(dto.page, total=len(event_id_list), records=data)

    @atomic()
    async def create(self, dto: CreateEventDTO, user: User, proj_list: list[Project]):
        """创建事件"""
        event_id = gid()
        # 创建参数
        param_tasks: list[BindParam] = []
        event_bind_param_tasks: list[EventBindParam] = []
        for p in dto.param_list:
            bid = gid()
            param_tasks.append(BindParam(id=bid, name=p.name,
                               description=p.description, type=p.type))
            event_bind_param_tasks.append(EventBindParam(
                id=gid(), event_id=event_id, bind_param_id=bid
            ))
        await BindParam.bulk_create(param_tasks)
        await EventBindParam.bulk_create(event_bind_param_tasks)
        # 创建事件
        await CustomEvent(id=event_id, name=dto.name, description=dto.description,
                          user_id=user.id, create_time=gnow(), update_time=gnow(), status=StatusEnum.NORMAL
                          ).save()
        # 添加到项目中
        await EventProject.bulk_create([
            EventProject(id=gid(), event_id=event_id, project_id=i.id) for i in proj_list
        ])

    @atomic()
    async def update(self, dto: UpdateEventDTO, event: CustomEvent, project_list: list[Project]):
        """修改自定义事件"""
        # 事件-项目
        await EventProject.filter(event_id=event.id).delete()
        if project_list:
            await EventProject.bulk_create([
                EventProject(id=gid(), event_id=event.id, project_id=i.id) for i in project_list
            ])
        # 事件-参数
        param_id_list = [i.bind_param_id for i in await EventBindParam.filter(event_id=event.id)]
        await BindParam.filter(id__in=param_id_list).delete()
        await EventBindParam.filter(event_id=event.id).delete()
        if dto.param_list:
            tasks1: list[BindParam] = []
            tasks2: list[EventBindParam] = []
            for p in dto.param_list:
                bpid = gid()
                tasks1.append(BindParam(id=bpid, **p.model_dump()))
                tasks2.append(EventBindParam(
                    id=gid(), event_id=event.id, bind_param_id=bpid))
            await BindParam.bulk_create(tasks1)
            await EventBindParam.bulk_create(tasks2)
        # 事件本身
        event.name = dto.name
        event.description = dto.description
        await event.save()
