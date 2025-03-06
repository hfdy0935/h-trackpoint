from fastapi_boot.core import Repository
from fastapi_boot.tortoise_util import Select

from domain.bo.project import EventOptionBO
from domain.entity.default_event import DefaultEvent
from domain.bo.event import BindParamBO, QueryEventDetailBO, QueryEventNameByProjectIdListBO
from domain.entity.custom_event import CustomEvent
from enums import StatusEnum
from constants import DB_NAME_DICT


@Repository
class DefaultEventDAO:
    """默认事件"""

    @Select("""
        SELECT de.*
        FROM {default_event} de
        JOIN {event_project} ep ON de.id = ep.event_id
        WHERE de.name IN {event_name_list}
          AND ep.project_id = {pid}
          AND de.status = {ok}
    """).fill_map(DB_NAME_DICT | dict(ok=StatusEnum.NORMAL))
    async def getByEventNameListAndProjId(
        self, event_name_list: list[str], pid: str) -> list[DefaultEvent]: ...
    # 根据事件名和项目id获取启用的默认事件

    @Select("""
        SELECT de.id, de.name, de.description, de.status, ep.project_id AS pid
        FROM {event_project} ep
        JOIN {default_event} de ON ep.event_id = de.id
        WHERE ep.project_id IN {proj_ids}
    """).fill_map(DB_NAME_DICT)
    async def getByProjIdList(
        self, proj_ids: list[str]) -> list[EventOptionBO]: ...
    # 根据项目id列表查询项目中的默认事件列表，用于修改项目时选择事件

    @Select("""
        SELECT t.*, GROUP_CONCAT(ep.project_id) AS pid_list, COUNT(ep.project_id) AS project_num
        FROM {event_project} ep
        JOIN (
            SELECT de.*, GROUP_CONCAT(ebp.bind_param_id) AS bpid_list, COUNT(ebp.bind_param_id) AS param_num
            FROM {default_event} de
            LEFT JOIN {event_bind_param} ebp ON de.id = ebp.event_id
            WHERE de.id IN {event_id_list}
            GROUP BY de.id
        ) t ON ep.event_id = t.id
        GROUP BY t.id
    """).fill_map(DB_NAME_DICT)
    async def getDetailByEventIdList(
        self, event_id_list: list[str]) -> list[QueryEventDetailBO]: ...
    # 根据默认事件id获取默认事件详情、绑定的参数id、事件所在项目id，（默认事件不考虑项目数量为0的情况，因为用户只有添加到项目中才能看到默认事件）

    @Select("""
        SELECT de.name
        FROM {default_event} de
        JOIN {event_project} ep ON de.id = ep.event_id
        WHERE ep.project_id IN {proj_id_list}
    """).fill_map(DB_NAME_DICT)
    async def getEventNameListByProjIdList(
        self, proj_id_list: list[str]) -> list[QueryEventNameByProjectIdListBO]: ...
    # 根据项目id列表获取项目中所有默认事件名列表


@Repository
class CustomEventDAO:
    """自定义事件"""

    @Select("""
        SELECT ce.*
        FROM {custom_event} ce
        JOIN {event_project} ep ON ce.id = ep.event_id
        WHERE ce.name IN {event_name_list}
          AND ep.project_id = {project_id}
          AND ce.status = {ok}
    """).fill_map(DB_NAME_DICT | dict(ok=StatusEnum.NORMAL))
    async def getByEventNameListAndProjId(
        self, event_name_list: list[str], project_id: str) -> list[CustomEvent]: ...
    # 根据事件名和项目id获取启用的自定义事件

    @Select("""
        SELECT ce.id, ce.name, ce.description, ce.status, ep.project_id AS pid
        FROM {event_project} ep
        JOIN {custom_event} ce ON ep.event_id = ce.id
        WHERE ep.project_id IN {proj_ids}
    """).fill_map(DB_NAME_DICT)
    async def getByProjIdList(
        self, proj_ids: list[str]) -> list[EventOptionBO]: ...
    # 根据项目id列表查询项目中的自定义事件列表，用于查询项目列表

    @Select("""
        SELECT t.*, GROUP_CONCAT(ep.project_id) AS pid_list, COUNT(ep.project_id) AS project_num
        FROM {event_project} ep
        RIGHT JOIN (
            SELECT ce.*, GROUP_CONCAT(ebp.bind_param_id) AS bpid_list, COUNT(ebp.bind_param_id) AS param_num
            FROM {custom_event} ce
            LEFT JOIN {event_bind_param} ebp ON ebp.event_id = ce.id
            WHERE ce.id IN {event_id_list}
            GROUP BY ce.id
        ) t ON ep.event_id = t.id
        GROUP BY t.id
    """).fill_map(DB_NAME_DICT)
    async def getDetailByEventIdList(
        self, event_id_list: list[str]) -> list[QueryEventDetailBO]: ...
    # 根据自定义事件id获取事件详情、绑定的参数id、事件所在项目id，考虑项目和参数数量为0的事件

    @Select("""
        SELECT ce.name
        FROM {custom_event} ce
        JOIN {event_project} ep ON ce.id = ep.event_id
        WHERE ep.project_id IN {proj_id_list}
    """).fill_map(DB_NAME_DICT)
    async def getEventNameListByProjIdList(
        self, proj_id_list: list[str]) -> list[QueryEventNameByProjectIdListBO]: ...
    # 根据项目id列表获取项目中所有自定义事件名列表


@Repository
class EventDAO:
    """通用查询"""
    @Select("""
        SELECT bp.id, bp.name, bp.description, bp.type, ebp.event_id AS eid
        FROM {bind_param} bp
        JOIN {event_bind_param} ebp ON ebp.bind_param_id = bp.id
        WHERE ebp.event_id IN {event_id_list}
    """).fill_map(DB_NAME_DICT)
    async def getBindParamListByEventIdList(
        self, event_id_list: list[str]) -> list[BindParamBO]: ...
    """根据事件id列表获取绑定参数列表"""
