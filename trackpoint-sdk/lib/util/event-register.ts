import type { ISendEventParams } from "../type/event";

/**
 * 注册DOM事件
 * @param element DOM元素
 * @param eventName 事件名称
 * @param callback 回调函数
 */
export function register(
  element: HTMLElement,
  eventName: string,
  callback: (event: ISendEventParams) => void
): void {
  element.addEventListener(eventName, (e: Event) => {
    const target = e.target as HTMLElement;
    callback({
      eventName,
      params: {
        elementId: target.id || '',
        elementTag: target.tagName.toLowerCase(),
        elementClass: target.className,
        elementText: target.textContent || '',
        elementValue: (target as HTMLInputElement).value || '',
        elementHref: (target as HTMLAnchorElement).href || '',
        timestamp: Date.now(),
        url: window.location.href,
        title: document.title
      }
    });
  });
} 