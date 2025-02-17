import type { BaseResp } from '@/type/base'
import type {
  IPerformanceMonitorItem,
  IPerformanceMonitorPerPage,
} from '@/type/data/performanceMonitor'
import { request } from '@/util/request'

/**
 * 性能监控统计信息
 */
export const reqPerformanceMonitorStat = (projectId: string) => {
  return request<IPerformanceMonitorItem, BaseResp<IPerformanceMonitorItem>, null>({
    url: '/data/performance-monitor',
    method: 'GET',
    params: { projectId },
  })
}

/**
 * 请求每个页面的性能指标
 */
export const reqPerformanceMonitorPerPage = (projectId: string) => {
  return request<IPerformanceMonitorPerPage[], BaseResp<IPerformanceMonitorPerPage[]>, null>({
    url: '/data/performance-monitor/per-page',
    method: 'GET',
    params: { projectId },
  })
}
