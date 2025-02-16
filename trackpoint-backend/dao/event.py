from fastapi_boot.core import Repository
from fastapi_boot.tortoise_util import Select

from domain.bo.project import EventOptionBO
from domain.entity.bind_param import BindParam
from domain.entity.default_event import DefaultEvent
from domain.entity.event_project import EventProject
from domain.entity.eventbind_param import EventBindParam
from domain.bo.event import BindParamBO, QueryEventDetailBO, QueryEventNameByProjectIdListBO
from domain.entity.custom_event import CustomEvent
from enums import StatusEnum


@Repository
class DefaultEventDAO:
    """默认事件"""

    @Select("""
        select de.* from {default_event} de, {event_project} ep
            where de.id = ep.event_id and de.name in {event_name_list} and ep.project_id = {pid} and de.status = {ok}
    """).fill(default_event=DefaultEvent.Meta.table, event_project=EventProject.Meta.table, ok=StatusEnum.NORMAL)
    async def getByEventNameListAndProjId(self, event_name_list: list[str],
                                          pid: str) -> list[DefaultEvent]: ...
    # 根据事件名和项目id获取启用的默认事件

    @Select("""
            select de.id,de.name,de.description,de.status, ep.project_id pid from {event_project} ep, {default_event} de
            where ep.project_id in {proj_ids} and ep.event_id = de.id
    """).fill(event_project=EventProject.Meta.table, default_event=DefaultEvent.Meta.table)
    async def getByProjIdList(
        self, proj_ids: list[str]) -> list[EventOptionBO]: ...
    # 根据项目id列表查询项目中的默认事件列表，用于修改项目时选择事件

    @Select("""
            select t.*, group_concat(ep.project_id) pid_list, count(ep.project_id) project_num from {event_project} ep,
            (select de.*, group_concat(ebp.bind_param_id) bpid_list, count(ebp.bind_param_id) param_num
                from {default_event} de
                left join {event_bind_param} ebp on de.id=ebp.event_id
                where de.id in {event_id_list}
                group by de.id) t
            where ep.event_id=t.id
             group by t.id
    """).fill(event_project=EventProject.Meta.table, default_event=DefaultEvent.Meta.table, bind_param=BindParam.Meta.table, event_bind_param=EventBindParam.Meta.table)
    async def getDetailByEventIdList(
        self, event_id_list: list[str]) -> list[QueryEventDetailBO]: ...
    # 根据默认事件id获取默认事件详情、绑定的参数id、事件所在项目id，（默认事件不考虑项目数量为0的情况，因为用户只有添加到项目中才能看到默认事件）

    @Select("""
        select de.name from {default_event} de, {event_project} ep
            where de.id=ep.event_id and ep.project_id in {proj_id_list}
    """).fill(default_event=DefaultEvent.Meta.table, event_project=EventProject.Meta.table)
    async def getEventNameListByProjIdList(
        self, proj_id_list: list[str]) -> list[QueryEventNameByProjectIdListBO]: ...
    # 根据项目id列表获取项目中所有默认事件名列表


@Repository
class CustomEventDAO:
    """自定义事件"""

    @Select("""
        select e.* from {event} e,{event_rpoject} ep
            where e.id = ep.event_id
            and ep.project_id = {project_id}
            and e.name in {event_name_list}
            and e.status={ok}
    """).fill(event=CustomEvent.Meta.table, event_rpoject=EventProject.Meta.table, ok=StatusEnum.NORMAL)
    async def getByEventNameListAndProjId(
        self,  event_name_list: list[str], project_id: str) -> list[CustomEvent]: ...
    # 根据事件名和项目id获取启用的自定义事件

    @Select("""
            select ce.id,ce.name,ce.description,ce.status, ep.project_id pid from {event_project} ep, {custom_event} ce
            where ep.project_id in {proj_ids} and ep.event_id = ce.id
    """).fill(event_project=EventProject.Meta.table, custom_event=CustomEvent.Meta.table)
    async def getByProjIdList(
        self, proj_ids: list[str]) -> list[EventOptionBO]: ...
    # 根据项目id列表查询项目中的自定义事件列表，用于查询项目列表

    @Select("""
            SELECT 
                t.*, 
                GROUP_CONCAT(ep.project_id) AS pid_list, 
                COUNT(ep.project_id) AS project_num 
            FROM 
                {event_project} ep
                RIGHT JOIN (
                    SELECT 
                        ce.*, 
                        GROUP_CONCAT(ebp.bind_param_id) AS bpid_list, 
                        COUNT(ebp.bind_param_id) AS param_num
                    FROM 
                        {custom_event} ce
                    LEFT JOIN 
                        {event_bind_param} ebp ON ebp.event_id = ce.id
                    WHERE 
                        ce.id IN {event_id_list}
                    GROUP BY 
                        ce.id
                ) t ON ep.event_id = t.id
            GROUP BY 
                t.id
    """).fill(event_project=EventProject.Meta.table, custom_event=CustomEvent.Meta.table, bind_param=BindParam.Meta.table, event_bind_param=EventBindParam.Meta.table)
    async def getDetailByEventIdList(
        self, event_id_list: list[str]) -> list[QueryEventDetailBO]: ...
    # 根据自定义事件id获取事件详情、绑定的参数id、事件所在项目id，考虑项目和参数数量为0的事件

    @Select("""
        select ce.name from {custom_event} ce, {event_project} ep
            where ce.id=ep.event_id and ep.project_id in {proj_id_list}
    """).fill(custom_event=CustomEvent.Meta.table, event_project=EventProject.Meta.table)
    async def getEventNameListByProjIdList(
        self, proj_id_list: list[str]) -> list[QueryEventNameByProjectIdListBO]: ...
    # 根据项目id列表获取项目中所有自定义事件名列表


@Repository
class EventDAO:
    """通用查询"""
    @Select("""
        select bp.id,bp.name,bp.description,bp.type,ebp.event_id eid from {bind_param} bp,{event_bind_param} ebp
            where ebp.event_id in {event_id_list}
            and ebp.bind_param_id = bp.id
    """).fill(bind_param=BindParam.Meta.table, event_bind_param=EventBindParam.Meta.table)
    async def getBindParamListByEventIdList(
        self, event_id_list: list[str]) -> list[BindParamBO]: ...
    """根据事件id列表获取绑定参数列表"""
