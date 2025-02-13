import type { BaseResp } from '@/type/base'
import type { IEvent } from '@/type/event'
import { request } from '@/util/request'

/**
 * 获取自定义事件列表，用于调试自定义事件
 * @param pid 项目id
 * @returns
 */
export function reqTestEventList(pid: string) {
  return request<IEvent[], BaseResp<IEvent[]>>({
    url: `/test/event-list`,
    method: 'get',
    params: { pid },
  })
}
