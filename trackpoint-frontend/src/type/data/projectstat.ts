import type { StatusEnum } from '@/enum'

/**
 * 项目统计中的单个项目
 */
export interface IProjectStat {
  id: string
  name: string
  status: StatusEnum
  create_time: string
  /**
   * 默认事件数量
   */
  default_count: number
  /**
   * 自定义事件数量
   */
  custom_count: number
  /**
   * 记录数量
   */
  record_count: number
  /**
   * 客户端数量
   */
  client_count: number
  /**
   * 所有默认performance事件的总时间，ms
   */
  performance_total_time: number
  /**
   * 所有默认performance事件的js内存占比，单位%
   */
  performance_js_rate: number
  /**
   * 请求报错率，单位%
   */
  request_error_rate: number
  /**
   * js报错次数
   */
  js_error_count: number
}
