import type { TimePeriod } from '../base'

/**
 * 单个客户端设备
 */
export interface IClient {
  id: string
  os: string
  os_version: string
  browser: string
  browser_version: string
  device: string
  lng: number
  lat: number
}

/**
 * 分析用户行为请求体
 */
export interface ReqUserBehaviorAnalysis {
  /**
   * 项目id
   */
  projectId: string
  /**
   * 事件id
   */
  eventId: string
  /**
   * 时间范围
   */
  timePeriod?: TimePeriod
}

/**
 * 分析用户行为响应体
 */
export interface RespUserBehaviorAnalysis {
  /**
   * 访问计数
   */
  visit: { time: string; pv: number; uv: number }[]
  /**
   * 可查询的点击数据
   */
  click: {
    url: string
    wh: [number, number][]
  }[]
  /**
   * 页面停留时间
   */
  stay: {
    page_url: string
    // 单位： s
    max: number
    min: number
  }[]
}

/**
 * 获取点击记录和图片请求体
 */
export interface ReqClickRecord extends ReqUserBehaviorAnalysis {
  url: string
  width: number
  height: number
}

/**
 * 获取点击记录和图片响应体
 */
export interface RespClickRecord {
  /**
   * 页面url
   */
  url: string
  /**
   * 截图url
   */
  src: string
  wh: [number, number]
  xy: [number, number][]
}
