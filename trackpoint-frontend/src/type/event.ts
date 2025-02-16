import type { EventTypeEnum, StatusEnum } from '@/enum'
import type { PageVO } from './base'
import type { ReqProjectList } from './project'

/**
 * 请求查询事件请求体
 */
export interface ReqEventList extends ReqProjectList {
  /**
   * 默认事件还是自定义事件
   */
  type: EventTypeEnum
  /**
   * 所属项目id列表，空表示所有项目
   */
  projectIdList?: string[]
}

/**
 * 用户事件单个绑定参数的类型
 */
export interface IBindParams {
  id: string
  name: string
  description: string
  /**
   * 参数类型
   */
  type: 'number' | 'string' | 'boolean' | 'array' | 'object'
  /**
   * 事件id
   */
  eid: string
}

/**
 * 单个项目选项
 */
export interface IProjectOption {
  id: string
  name: string
  /**
   * 事件id
   */
  eid: string
  status: StatusEnum
}

/**
 * 事件列表中的单个事件
 */
export interface IEvent {
  id: string
  name: string
  description: string
  status: StatusEnum
  create_time: string
  update_time: string
  /**
   * 事件绑定的参数列表
   */
  param_list: IBindParams[]
  /**
   * 参数数量
   */
  param_num: number
  /**
   * 事件所属项目列表
   */
  project_list: IProjectOption[]
  /**
   * 该事件被几个项目使用
   */
  project_num: number
}

/**
 * 获取事件列表响应体
 */
export interface RespEventList extends PageVO<IEvent> {}

/**
 * 修改事件状态
 */
export interface ReqUpdateEventStatus {
  id: string
  status: StatusEnum
}

/**
 * 事件参数类型
 */
export type EventParamType = 'number' | 'string' | 'boolean' | 'array' | 'object'
/**
 * 创建事件请求体
 */
export interface ReqCreateEvent {
  name: string
  description: string
  paramList: Omit<Omit<IBindParams, 'eid'>, 'id'>[]
  projectIdList: string[]
}

/**
 * 更新事件请求体
 */
export interface ReqUpdateEvent extends ReqCreateEvent {
  id: string
}
