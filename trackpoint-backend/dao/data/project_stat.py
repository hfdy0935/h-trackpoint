from fastapi_boot.core import Repository
from fastapi_boot.tortoise_util import Select

from domain.vo.data.project_stat import ProjectStatVO
from constants import DB_NAME_DICT


@Repository
class DataDAO:
    @Select("""
        SELECT t1.id, t1.name,t1.status,
            t1.record_count record_count,
            t1.client_count client_count,
            t1.create_time,
            t2.default_count default_count,
            t2.custom_count custom_count,
            COALESCE(t3.performance_total_time,-1) performance_total_time,
            COALESCE(t3.performance_js_rate,-1) performance_js_rate,
            COALESCE(t4.request_error_rate,-1) request_error_rate,
            COALESCE(t5.js_error_count,-1) js_error_count
        FROM (
            SELECT p.id,
                p.name,
                p.status,
                p.create_time,
                COUNT(r.id) AS record_count,
                COUNT(DISTINCT r.client_id) AS client_count
            FROM {record} r
            RIGHT JOIN {project} p ON p.id = r.project_id
            GROUP BY p.id
        ) t1
        LEFT JOIN (
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
        ) t2 on t1.id=t2.id
        LEFT JOIN (
            SELECT p.id AS id,
                p.name AS name,
                AVG(JSON_UNQUOTE(JSON_EXTRACT(r.params, '$.dns')) + JSON_UNQUOTE(JSON_EXTRACT(r.params, '$.tcp')) 
                + JSON_UNQUOTE(JSON_EXTRACT(r.params, '$.request')) + JSON_UNQUOTE(JSON_EXTRACT(r.params, '$.response')) 
                + JSON_UNQUOTE(JSON_EXTRACT(r.params, '$.processing')) + JSON_UNQUOTE(JSON_EXTRACT(r.params, '$.load_event_duration')) 
                ) AS performance_total_time,
                AVG(JSON_UNQUOTE(JSON_EXTRACT(r.params, '$.js_heap_size_used_percent')))/100 AS performance_js_rate
            FROM {project} p
            JOIN {record} r ON p.id = r.project_id
            JOIN (SELECT id FROM {default_event} de WHERE de.name = 'performance') de ON r.event_id = de.id
            WHERE p.user_id = {user_id}
            GROUP BY p.id
        ) t3 on t1.id=t3.id
        LEFT JOIN(
            SELECT p.id AS id,
                p.name AS name,
                SUM(CASE WHEN JSON_UNQUOTE(JSON_EXTRACT(r.params, '$.status_code')) != '200' THEN 1 ELSE 0 END) / COUNT(*) AS request_error_rate
            FROM {project} p
            JOIN {record} r ON p.id = r.project_id
            JOIN (SELECT id FROM {default_event} de WHERE de.name = 'request') de ON r.event_id = de.id
            WHERE p.user_id = {user_id}
            GROUP BY p.id
        ) t4 on t1.id=t4.id
        LEFT JOIN  (
            SELECT p.id AS id,
                p.name AS name,
                COUNT(*) AS js_error_count
            FROM {project} p
            JOIN {record} r ON p.id = r.project_id
            JOIN (SELECT id FROM {default_event} de WHERE de.name = 'js_error') de ON r.event_id = de.id
            WHERE p.user_id = {user_id}
            GROUP BY p.id
        ) t5 on t1.id=t5.id
    """).fill_map(DB_NAME_DICT)
    async def getProjectEventStat(
        self, user_id: str) -> list[ProjectStatVO]: ...
    # 查询用户每个项目中事件的统计信息
