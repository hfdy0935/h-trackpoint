import type { AxiosResponse } from "axios";
import { type BaseResp, type ICommonParams } from "./common";
import { type IRegister } from "./register";

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
 * 上报事件请求体
 */
export interface ReqSendEvent extends Omit<IRegister, "uploadPercent"> {
  uid: string;
  eventName: string;
  params: ICommonParams;
  pageUrl: string;
  createTime: string;
}

/**
 * 上报事件响应体
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
