import type { ReqRecordList, IProjectEventInfo, RespRecordList } from '@/type/record'
import type { BaseResp } from '@/type/base'
import { request } from '@/util/request'

/**
 * 获取用户各项目下的事件，用于筛选上报记录
 * @returns
 */
export function reqProjectEventInfo() {
  return request<IProjectEventInfo[], BaseResp<IProjectEventInfo[]>>({
    url: '/record/proj-event-detail',
    method: 'get',
  })
}

/**
 * 查询上报事件记录列表
 * @returns
 */
export function reqRecordList(data: ReqRecordList) {
  return request<RespRecordList, BaseResp<RespRecordList>, ReqRecordList>({
    url: '/record/list',
    method: 'post',
    data,
  })
}

/**
 * 根据id删除上报事件记录
 * @returns
 */
export function reqDeleteRecord(id: string) {
  return request<null, BaseResp<null>, { id: string }>({
    url: `/record/${id}`,
    method: 'delete',
  })
}
