import { sendEvent } from '@/h-trackpoint/main'
import type { Directive } from 'vue'

interface ReqSendClickEvent {
  x: number
  y: number
  w: number
  h: number
}
/**
 * 手动上报点击事件
 * @param e
 */
const doSendClickEvent = async (e: MouseEvent) => {
  await sendEvent<ReqSendClickEvent>('click', {
    x: e.clientX,
    y: e.clientY,
    w: window.innerWidth,
    h: window.innerHeight,
  })
}

/**
 * 上报点击事件的指令
 */
export const sendClickEventDirective: Directive = {
  mounted(el: HTMLElement) {
    el.addEventListener('click', doSendClickEvent)
  },
  beforeUnmount(el: HTMLElement) {
    el.removeEventListener('click', doSendClickEvent)
  },
}
