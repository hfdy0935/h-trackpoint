import type { BaseResp } from "@/type/base"
import type { RespBaseStat } from "@/type/data/stat/base"
import type { IEventStat } from "@/type/data/stat/event"
import type { IProjectStat } from "@/type/data/stat/project"
import { request } from "@/util/request"

/**
 * 获取基本统计信息
 */
export const reqBaseStat = () => {
    return request<BaseResp<RespBaseStat>, BaseResp<RespBaseStat>, null>({
        url: '/data/base-stat',
        method: 'GET'
    })
}


/**
 * 获取项目统计信息
 */
export const reqProjectStat = () => {
    return request<BaseResp<IProjectStat[]>, BaseResp<IProjectStat[]>, null>({
        url: '/data/project-stat',
        method: 'GET'
    })
}

/**
 * 获取事件统计信息
 */
export const reqEventStat = () => {
    return request<BaseResp<IEventStat[]>, BaseResp<IEventStat[]>, null>({
        url: '/data/event-stat',
        method: 'GET'
    })
}