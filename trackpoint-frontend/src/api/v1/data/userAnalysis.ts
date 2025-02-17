import type { BaseResp } from '@/type/base'
import type {
  IClient,
  ReqClickRecord,
  ReqUserBehaviorAnalysis,
  RespClickRecord,
  RespUserBehaviorAnalysis,
} from '@/type/data/userAnalysis'
import { request } from '@/util/request'

/**
 * 获取项目下的用户
 */
export const reqUserAnalysisUserList = (projectId: string) => {
  return request<IClient[], BaseResp<IClient[]>, null>({
    url: '/data/user-analysis/distribution',
    method: 'GET',
    params: { projectId },
  })
}

/**
 * 分析用户行为
 */
export const reqUserBehaviorAnalysis = (data: ReqUserBehaviorAnalysis) => {
  return request<
    RespUserBehaviorAnalysis,
    BaseResp<RespUserBehaviorAnalysis>,
    ReqUserBehaviorAnalysis
  >({
    url: '/data/user-analysis/behavior',
    method: 'POST',
    data,
  })
}

/**
 * 获取用户点击数据
 */
export const reqUserClickData = (data: ReqClickRecord) => {
  return request<RespClickRecord, BaseResp<RespClickRecord>, ReqClickRecord>({
    url: '/data/user-analysis/click-data',
    method: 'POST',
    data,
  })
}
