import type { StatusEnum } from "@/enum"
import type { OrderBy, PageQuery, PageVO, TimePeriod } from "./base"

/**
 * 查询项目列表请求体
 */
export interface ReqProjectList {
    /**
     * 搜索关键词
     */
    keyword?: string
    /**
     * 状态
     */
    status: StatusEnum[]
    /**
     * 字段排序
     */
    orderBy?: OrderBy[]
    /**
     * 创建时间范围
     */
    createTimePeriod?: TimePeriod
    /**
     * 更新时间范围
     */
    updateTimePeriod?: TimePeriod
    /**
     * 分页
     */
    page: PageQuery
}

/**
 * 单个事件选项
 */
export interface IEventOption {
    id: string
    name: string
    pid: string // 没用到
    status: StatusEnum // 没用到
}
/**
 * 用于创建/修改项目时选择默认/自定义事件
 */
export interface RespEventOpions {
    default: IEventOption[]
    custom: IEventOption[]
}
/**
 * 项目列表中的单个项目类型
 */
export interface IProject {
    id: string
    name: string
    /**
     * 项目状态
     */
    status: StatusEnum
    description: string
    create_time: string
    update_time: string
    /**
     * 该项目的事件列表
     */
    event_list: IEventOption[]
    event_num: number
}
/**
 * 请求项目列表的响应体
 */
export interface RespProjectList extends PageVO<IProject> {
}

/**
 * 创建项目请求体
 */
export interface ReqCreateProject {
    /**
     * 项目名
     */
    name: string
    /**
     * 项目描述
     */
    description: string
    /**
     * 默认事件id列表
     */
    defaultEventIdList: string[]
    /**
     * 自定义事件id列表
     */
    customEventIdList: string[]
}

/**
 * 创建项目响应体
 */
export interface RespCreateProject {
    /**
     * 项目id
     */
    id: string
    /**
     * 项目key，只能看一次
     */
    key: string
}


/**
 * 修改项目信息请求体
 */
export interface ReqUpdateProject {
    id: string
    name: string
    description: string
    /**
     * 默认事件id列表
     */
    defaultEventIdList: string[]
    /**
     * 自定义事件id列表
     */
    customEventIdList: string[]
}

/**
 * 修改项目状态，请求参数少，和其他的不在一块，就分开写了
 */
export interface ReqUpdateProjectStatus {
    id: string
    status: StatusEnum
}