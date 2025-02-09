import { DEFAULT_REGISTER_CONFIG } from "../constants";
import { type ICommonParams } from "../type/common";
import { type IRegister } from "../type/register";
import { getUserBaseInfo } from "../util/register";
import { getInstance, ProjectInstanceImpl } from "./project";
import { EventQueue } from "./queue";

let eventQueue: EventQueue;

/**
 * 注册项目
 * @param options 项目配置
 */
export async function register(options: IRegister): Promise<void> {
  const mergedOptions = {
    ...DEFAULT_REGISTER_CONFIG,
    ...options,
  };
  
  // 创建事件队列实例，使用配置中的参数
  eventQueue = new EventQueue({
    maxRetries: mergedOptions.maxRetries,
    batchSize: mergedOptions.batchSize,
    flushInterval: mergedOptions.flushInterval,
    retryInterval: mergedOptions.retryInterval,
  });

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
  if (!eventQueue) {
    throw new Error('请先调用 register 初始化 SDK');
  }
  
  // 合并通用参数
  const mergedParams = {
    ...getInstance().commonParams,
    ...params
  };
  
  eventQueue.enqueue({
    eventName,
    params: mergedParams,
  });
}

// 在页面卸载时确保队列中的事件都被处理
window.addEventListener('beforeunload', () => {
  eventQueue?.destroy();
});
