export interface DescriptionNumber {
  max: number
  min: number
  avg: number
}

/**
 * 基本性能统计数据
 */
export interface IPerformanceMonitorItem {
  dns: DescriptionNumber
  tcp: DescriptionNumber
  request: DescriptionNumber
  response: DescriptionNumber
  processing: DescriptionNumber
  load_event_duration: DescriptionNumber
  js_heap_size_used_percent: DescriptionNumber
}

/**
 * 每个页面的性能指标
 */
export interface IPerformanceMonitorPerPage {
  page_url: string
  performance: IPerformanceMonitorItem
}
