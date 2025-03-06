import { type ICommonParams } from '../type/common';
import { type IRegister } from '../type/register';
/**
 * 注册项目
 * @param options 项目配置
 */
export declare function register(options: IRegister): Promise<void>;
/**
 * 添加通用参数
 * @param params
 */
export declare function addCommonParams<T extends ICommonParams = ICommonParams>(params: T): void;
/**
 * 上报事件
 * @param eventName
 * @param params
 */
export declare function sendEvent<T extends ICommonParams = ICommonParams>(eventName: string, params: T): Promise<void>;
