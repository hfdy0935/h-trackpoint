import type { ARB } from '../type/common';
import type { BatchSendEventsRequest, RespSendEvent } from '../type/event';
import type { IRegister, UserBaseInfo } from '../type/register';
import { DefaultEventNameEnum } from '../enum';
/**
 * 注册项目
 * @param options 项目配置
 * @param baseInfo 用户基本信息
 * @returns Promise
 */
export declare function reqRegister(options: IRegister, baseInfo: UserBaseInfo): Promise<ARB<DefaultEventNameEnum[]>>;
/**
 * 批量上报事件
 * @param data 事件数据，包含用户ID、项目ID和事件数组
 */
export declare function reqSendEvents(data: BatchSendEventsRequest): Promise<ARB<RespSendEvent>>;
/**
 * 上传截图
 * @param rid 之前上报事件的记录id
 */
export declare function reqSendScreenshot(rids: string[]): Promise<void>;
