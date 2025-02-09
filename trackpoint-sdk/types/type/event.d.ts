import { type ICommonParams } from "./common";
/**
 * 发送请求上报事件函数的参数
 */
export interface ISendEventParams {
    /**
     * 事件名
     */
    eventName: string;
    /**
     * 事件参数
     */
    params: ICommonParams;
}
/**
 * 批量上报的事件项
 */
export interface BatchEventItem {
    /**
     * 事件名
     */
    eventName: string;
    /**
     * 事件参数
     */
    params: ICommonParams;
    /**
     * 页面URL
     */
    pageUrl: string;
    /**
     * 创建时间戳
     */
    createTime: number;
}
/**
 * 批量上报请求体
 */
export interface BatchSendEventsRequest {
    events: BatchEventItem[];
}
/**
 * 单个事件响应
 */
export interface RespSendEvent {
    /**
     * 记录id
     */
    record_id: string;
    /**
     * 是否需要上传截图
     */
    need_upload_shot: boolean;
}
/**
 * 上报的performance类型，参考https://juejin.cn/post/6844904182202253325，单位都是毫秒
 */
export interface ISendPerformanceEvent {
    dns: number;
    tcp: number;
    request: number;
    response: number;
    processing: number;
    load_event_duration: number;
    /**
     * 额外加一个js堆占用百分比
     */
    js_heap_size_used_percent: number;
}
