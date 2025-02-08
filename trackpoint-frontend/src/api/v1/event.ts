import type { BaseResp } from "@/type/base";
import type { ReqCreateEvent, ReqEventList, ReqUpdateEvent, ReqUpdateEventStatus, RespEventList } from "@/type/event";
import type { RespEventOpions } from "@/type/project";
import { request } from "@/util/request";


/**
 * 获取事件选项，用于创建/修改项目时选
 * @returns 
 */
export function reqEventOptions() {
    return request<undefined, BaseResp<RespEventOpions>>({
        url: '/event/option',
        method: 'get',
    })
}

/**
 * 条件查询事件列表
 * @param data 
 * @returns 
 */
export function reqEventList(data: ReqEventList) {
    return request<ReqEventList, BaseResp<RespEventList>>({
        url: '/event/list',
        method: 'post',
        data
    })
}

/**
 * 删除事件
 * @param id 项目id 
 * @returns 
 */
export function reqDeleteEvent(id: string) {
    return request<string, BaseResp<null>>({
        url: `/event/${id}`,
        method: 'delete',
    })
}


/**
 * 修改事件状态
 * @param data 
 * @returns 
 */
export function reqUpdateEventStatus(data: ReqUpdateEventStatus) {
    return request<ReqUpdateEventStatus, BaseResp<null>>({
        url: '/event/status',
        method: 'put',
        data
    })
}


/**
 * 创建事件
 * @param data 
 */
export function reqCreateEvent(data: ReqCreateEvent) {
    return request<ReqCreateEvent, BaseResp<null>>({
        url: '/event',
        method: 'post',
        data
    })
}

/**
 * 修改事件
 * @param data 
 */
export function reqUpdateEvent(data: ReqUpdateEvent) {
    return request<ReqUpdateEvent, BaseResp<null>>({
        url: '/event',
        method: 'put',
        data
    })
}