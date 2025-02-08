import type { TimePeriod } from "../../base"

/**
 * 根据参数过滤记录
 */
export interface IFilterEventParamItem {
    /**
     * 参数名
     */
    name: string
    /**
     * 值，目前只考虑等于
     */
    value: any
}
/**
 * 获取记录统计信息的请求体
 */
export interface ReqDataStat2 {
    projectId: string
    eventId: string
    /**
     * 时间范围
     */
    timePeriod: TimePeriod
    /**
     * 时间粒度
     */
    timeGranularity: 'hour' | 'day' | 'month'
    /**
     * 根据参数过滤
     */
    filterParamList: IFilterEventParamItem[]

}

/**
 * 记录统计中的单个事件记录
 */
export interface IRecord {
    id: string
    /**
     * 所属项目id
     */
    project_id: string
    /**
     * 所属事件id
     */
    event_id: string
    // /**
    //  * 客户端信息
    //  */
    // client: IClient
    /**
     * 上报时间
     */
    send_time: string
    /**
     * 页面url
     */
    page_url: string
    /**
     * 参数
     */
    params: {}
}

/**
 * 获取记录统计信息响应体
 */
export interface RespDataStat2 {
    /**
    * 所属项目id
    */
    project_id: string
    /**
     * 所属事件id
     */
    event_id: string
    /**
     * 记录列表
     */
    record_list: IRecord[]
}
