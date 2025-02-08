import { DEFAULT_REGISTER_CONFIG } from "../constants";
import { type ICommonParams } from "../type/common";
import { type IRegister } from "../type/register";
import { getUserBaseInfo } from "../util/register";
import { reqSendEvent } from "./http";
import { getInstance, ProjectInstanceImpl } from "./project";


/**
 * 注册项目
 * @param options 项目配置
 */
export async function register(options: IRegister): Promise<void> {
  const mergedOptions = {
    ...DEFAULT_REGISTER_CONFIG,
    ...options,
  };
  await ProjectInstanceImpl.create(mergedOptions, await getUserBaseInfo());
}

/**
 * 添加通用参数
 * @param params
 */
export function addCommonParams<T extends ICommonParams = ICommonParams>(params: T): void {
  getInstance().addCommonParams(params);
}

/**
 * 上报事件
 * @param eventName
 * @param params
 */
export async function sendEvent<T extends ICommonParams = ICommonParams>(eventName: string, params: T) {
  await reqSendEvent({
    eventName,
    params,
  });
}
