import type { ARB } from "../type/common";
import type { ISendEventParams, RespSendEvent } from "../type/event";
import type { IRegister, UserBaseInfo } from "../type/register";
import { DefaultEventNameEnum } from "../enum";
/**
 * 注册项目
 * @param options 项目id、key、上传频率（暂时没用到）
 * @param props 用户传的配置，注册成功、失败、报错时的回调函数
 * @param baseInfo 用户基本信息，用于注册客户端
 * @returns Promise
 */
export declare function reqRegister(options: IRegister, baseInfo: UserBaseInfo): Promise<ARB<DefaultEventNameEnum[]>>;
/**
 * 上报事件
 * @param props 事件名和参数
 */
export declare function reqSendEvent(props: ISendEventParams): Promise<ARB<RespSendEvent>>;
/**
 * 上传截图
 * @param rid 之前上报事件的记录id
 */
export declare function reqSendScreenshot(rid: string): Promise<void>;
