import type { ARB } from "../type/common";
import type { BatchEventItem, RespSendEvent } from "../type/event";
import type { IRegister, UserBaseInfo } from "../type/register";
import { DefaultEventNameEnum } from "../enum";
/**
 * 注册项目
 * @param options 项目id、key、上传频率（暂时没用到）
 * @param baseInfo 用户基本信息，用于注册客户端
 * @returns Promise
 */
export declare function reqRegister(options: IRegister, baseInfo: UserBaseInfo): Promise<ARB<DefaultEventNameEnum[]>>;
/**
 * 批量上报事件
 * @param events 事件数组
 */
export declare function reqSendEvents(events: BatchEventItem[]): Promise<ARB<RespSendEvent[]>>;
/**
 * 上传截图
 * @param rid 之前上报事件的记录id
 */
export declare function reqSendScreenshot(rid: string): Promise<void>;
