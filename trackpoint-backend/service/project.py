from datetime import datetime
from typing import Literal
from fastapi_boot.core import Service
from redis import Redis
from tortoise.transactions import atomic
from tortoise.queryset import QuerySet

from dao.event import CustomEventDAO, DefaultEventDAO
from dao.project import ProjectDAO
from domain.bo.project import EventOptionBO
from domain.dto.project import CreateProjectDTO, QueryProjectDTO, UpdateProjectDTO
from domain.entity.default_event import DefaultEvent
from domain.entity.project import Project
from domain.entity.user import User
from domain.entity.custom_event import CustomEvent
from domain.entity.event_project import EventProject
from domain.vo.common import PageVO
from domain.vo.project import CreateProjectVO, QueryProjectVO
from enums import StatusEnum
from exception import BusinessException
from tortoise.expressions import Q

from utils import MD5Util, gid, gnow


@Service
class ProjectService:

    def __init__(self, proj_dao: ProjectDAO, md5: MD5Util, ce_dao: CustomEventDAO, de_dao: DefaultEventDAO, redis: Redis) -> None:
        self.proj_dao = proj_dao
        self.md5 = md5
        self.ce_dao = ce_dao
        self.de_dao = de_dao
        self.redis = redis

    @atomic()
    async def create(self, user: User, dto: CreateProjectDTO, custom_event_list: list[CustomEvent]) -> CreateProjectVO:
        """创建项目

        Args:
            user (User): 所属用户实例
            dto (CreateProjectDTO): 请求体
            custom_event_list (list[CustomEvent]): 自定义事件列表，已经过权限验证

        Raises:
            BusinessException: 创建失败

        Returns:
            _type_: 响应体
        """
        # 如果达到上限（包括回收站的），创建失败
        project_num = await Project.filter(user_id=user.id).count()
        if project_num >= user.project_num_limit:
            raise BusinessException(detail='创建失败，项目数量已达上限')
        # 创建项目
        proj_id, key = gid(), gid()
        current = gnow()
        # 保存项目
        await Project(
            id=proj_id, name=dto.name, description=dto.description, user_id=user.id, key=self.md5.encrypt(
                key),
            create_time=current, update_time=current,
            status=StatusEnum.NORMAL
        ).save()
        # 给该项目添加用户希望加的默认事件和自定义事件
        default_event_list = await DefaultEvent.filter(id__in=dto.default_event_id_list, status=StatusEnum.NORMAL)
        await EventProject.bulk_create([EventProject(
            id=gid(), event_id=de.id, project_id=proj_id) for de in [*default_event_list, *custom_event_list]])
        return CreateProjectVO(id=proj_id, key=key)

    @atomic()
    async def delete(self, project: Project):
        """删除项目和事件项目记录"""
        await EventProject.filter(project_id=project.id).delete()
        await project.delete()

    async def list(self, user: User, dto: QueryProjectDTO) -> PageVO[QueryProjectVO]:
        """分页、条件查询用户的项目

        Args:
            user (User): _description_
            dto (QueryProjectDTO): _description_

        Returns:
            PageVO[QueryProjectVO]: _description_
        """
        qs = Project.filter(user_id=user.id)
        # 关键词
        kwd = dto.keyword
        if kwd and kwd.strip():
            qs = qs.filter(Q(name__icontains=kwd) | Q(
                description__icontains=kwd))
        # 状态
        if dto.status is not None:
            qs = qs.filter(status__in=dto.status)
        # 排序，antd vue只支持一个字段的排序，所以这里最多只有一个字段
        for order in dto.order_by:
            if order.field and order.order and order.field != 'event_num':
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
        # 总数量
        total_num = await qs.count()
        # 分页
        qs: QuerySet[Project] = dto.page.execute(qs)
        # 查询项目
        projects = await qs
        # 每个项目中的事件数量
        records: list[QueryProjectVO] = []
        if len(projects) > 0:
            proj_id_list = [i.id for i in projects]
            event_list: list[EventOptionBO] = [*await self.ce_dao.getByProjIdList(proj_id_list), *await self.de_dao.getByProjIdList(proj_id_list)]
            # 组装结果
            for p in projects:
                filter_event_list = list(
                    filter(lambda x: x.pid == p.id, event_list))
                records.append(QueryProjectVO(
                    id=p.id, name=p.name, description=p.description, status=p.status, create_time=p.create_time, update_time=p.update_time,
                    event_list=filter_event_list, event_num=len(
                        filter_event_list)
                ))
            if o := dto.has_event_num_and_order:
                records.sort(key=lambda x: x.event_num,
                             reverse=o == 'descend')
        return PageVO[QueryProjectVO].create(dto.page, total_num, records)

    @atomic()
    async def update(self, project: Project, dto: UpdateProjectDTO):
        """修改项目"""
        await project.update_from_dict({
            'name': dto.name,
            'description': dto.description or '',
            'update_time': datetime.now()
        }).save()
        # 删除该项目原来的事件记项目录
        await EventProject.filter(project_id=project.id).delete()
        # 添加新事件项目记录
        await EventProject.bulk_create(
            [EventProject(id=gid(), event_id=i, project_id=project.id)
             for i in [*dto.default_event_id_list, *dto.custom_event_id_list]]
        )
