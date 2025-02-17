import type { BaseResp } from '@/type/base'
import type { IProjectStat } from '@/type/data/projectstat'
import { request } from '@/util/request'

/**
 * 获取项目统计信息
 */
export const reqProjectStat = () => {
  return request<BaseResp<IProjectStat[]>, BaseResp<IProjectStat[]>, null>({
    url: '/data/project-stat',
    method: 'GET',
  })
}
