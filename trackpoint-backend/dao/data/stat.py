from fastapi_boot.core import Repository
from fastapi_boot.tortoise_util import Select

from domain.entity.client import Client
from domain.entity.custom_event import CustomEvent
from domain.entity.default_event import DefaultEvent
from domain.entity.event_project import EventProject
from domain.entity.project import Project
from domain.entity.record import Record
from domain.vo.data.stat.base import IClient
from domain.vo.data.stat.event import EventStatVO
from domain.vo.data.stat.project import ProjectStatVO


@Repository
class DataDAO:

    @Select("""
        select distinct c.* from {client} c,{project} p, {record} r
            where p.user_id={user_id} and r.project_id=p.id and c.id=r.client_id
    """).fill(client=Client.Meta.table, project=Project.Meta.table, record=Record.Meta.table)
    async def get_client_list_by_user_id(
        self, user_id: str) -> list[IClient]: ...
    # 根据用户id获取用户所有项目中的客户端列表，用于基本信息统计

    @Select("""
        SELECT t2.*,
            t1.record_count,
            t1.client_count
        FROM (
            SELECT p.id,
                COUNT(r.id) AS record_count,
                COUNT(DISTINCT r.client_id) AS client_count
            FROM {record} r
            RIGHT JOIN {project} p ON p.id = r.project_id
            GROUP BY p.id
        ) t1,
        (
            SELECT 
                p.id AS id,
                p.name AS name,
                SUM(CASE WHEN de.id IS NOT NULL THEN 1 ELSE 0 END) AS default_count,
                SUM(CASE WHEN ce.id IS NOT NULL THEN 1 ELSE 0 END) AS custom_count
            FROM {project} p
            LEFT JOIN {event_project} ep ON ep.project_id = p.id
            LEFT JOIN {default_event} de ON de.id = ep.event_id
            LEFT JOIN {custom_event} ce ON ce.id = ep.event_id
            WHERE p.user_id = {user_id}
            GROUP BY p.id, p.name
        ) t2
        WHERE t1.id = t2.id;
    """).fill(custom_event=CustomEvent.Meta.table, default_event=DefaultEvent.Meta.table, project=Project.Meta.table, event_project=EventProject.Meta.table, record=Record.Meta.table)
    async def getProjectEventStat(
        self, user_id: str) -> list[ProjectStatVO]: ...
    # 查询用户每个项目中事件的统计信息

    @Select("""
        SELECT 
        p.*,
        COUNT(r.id) AS record_count,
        COUNT(DISTINCT r.client_id) AS client_count
    FROM 
        project p
    LEFT JOIN 
        record r ON r.project_id = p.id
    WHERE 
        p.user_id = {user_id}
    GROUP BY 
        p.id;
    """)
    async def getProjectRecordClientStat(self, user_id: str): ...
    # 根据用户id获取每个项目中记录和客户端数量

    @Select("""
        select ce.id as id,ce.name as name,count(ep.id) as count
        from {custom_event} ce
        left join {event_project} ep on ep.event_id=ce.id
        where ce.user_id={user_id}
        group by ce.id
            union all
            select de.id as id,de.name as name,count(ep.id) as count
            from {default_event} de,{event_project} ep,{project} p
            where ep.event_id=de.id and ep.project_id=p.id and p.user_id={user_id}
            group by de.id
    """).fill(custom_event=CustomEvent.Meta.table, event_project=EventProject.Meta.table, default_event=DefaultEvent.Meta.table, project=Project.Meta.table)
    async def getProjCountGroupByEvent(
        self, user_id: str) -> list[EventStatVO]: ...
    # 查询用户每个事件的项目数量
