
import { DefaultEventNameEnum } from "../enum/index";
import type { ISendPerformanceEvent } from "../type/event";
import { sendEvent } from "./method";

/**
 * Performance.memory，来自vueuse
 *
 * @see https://developer.mozilla.org/en-US/docs/Web/API/Performance/memory
 */
interface MemoryInfo {
  /**
   * The maximum size of the heap, in bytes, that is available to the context.
   */
  readonly jsHeapSizeLimit: number;
  /**
   *  The total allocated heap size, in bytes.
   */
  readonly totalJSHeapSize: number;
  /**
   * The currently active segment of JS heap, in bytes.
   */
  readonly usedJSHeapSize: number;
  [Symbol.toStringTag]: 'MemoryInfo';
}

/**
 * 自动上报performance部分指标
 */
async function registerAutoSendPerformanceEvent() {
  if (!performance || !('memory' in performance)) return
  // 导航阶段 
  // @ts-ignore
  const nav: PerformanceNavigationTiming = performance.getEntries()[0]
  const memory = performance.memory as MemoryInfo
  const data: ISendPerformanceEvent = {
    dns: +(nav.domainLookupEnd - nav.domainLookupStart).toFixed(2),
    tcp: +(nav.connectEnd - nav.connectStart).toFixed(2),
    request: +(nav.responseStart - nav.requestStart).toFixed(2),
    response: +(nav.responseEnd - nav.responseStart).toFixed(2),
    processing: +(nav.domComplete - nav.domInteractive).toFixed(2),
    load_event_duration: +(nav.loadEventEnd - nav.loadEventStart).toFixed(2),
    js_heap_size_used_percent: +(memory.usedJSHeapSize / memory.totalJSHeapSize * 100).toFixed(2)
  };
  await sendEvent<ISendPerformanceEvent>(DefaultEventNameEnum.PERFORMANCE, data)
}


/**
 * 自动上报js报错
 */
function registerAutoSendJSErrorEvent() {
  window.addEventListener("error", async (e) => {
    if (e instanceof ErrorEvent) {
      sendEvent<{
        error_reason: string
      }>(DefaultEventNameEnum.JS_ERROR, {
        error_reason: e.message,
      });
    }
  });
}

/**
 * 需要自动上报的默认事件名: 函数 map，
 */
const defaultEventNameHandlerMap: Partial<Record<DefaultEventNameEnum, () => void>> = {
  js_error: registerAutoSendJSErrorEvent,
  performance: registerAutoSendPerformanceEvent
}

/**
 * 决定是否需要自动上报及自动上报的事件
 */
export function registerAutoSendEvents(defaultEventNameList: DefaultEventNameEnum[]) {
  defaultEventNameList.forEach((el) => {
    defaultEventNameHandlerMap[el]?.()
  });
}
