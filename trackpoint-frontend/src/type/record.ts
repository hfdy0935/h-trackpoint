import type { OrderBy, PageQuery, PageVO, TimePeriod } from './base'
import type { IClient } from './data/userAnalysis'

/**
 * 获取用户所有项目和事件id、名的单条记录
 */
export interface IProjectEventInfo {
  project_id: string
  project_name: string
  events: {
    event_id: string
    event_name: string
  }[]
}

/**
 * 过滤参数查询的单个参数
 */
export interface IFilterParam {
  name: string
  value: any
}
/**
 * 查询上报事件记录列表请求体
 */
export interface ReqRecordList {
  /**
   * 项目id
   */
  projectId: string
  /**
   * 事件id
   */
  eventId: string
  /**
   * 字段排序
   */
  orderBy?: OrderBy[]
  /**
   * 创建时间范围
   */
  createTimePeriod?: TimePeriod
  /**
   * 过滤参数
   */
  filterParamList: IFilterParam[]
  /**
   * 分页
   */
  page: PageQuery
}

/**
 * 获取上报记录响应体
 */
export interface RespRecordList
  extends PageVO<{
    id: string
    project_name: string
    event_name: string
    create_time: string
    client: IClient
    page_url: string
    params: {}
  }> {}
