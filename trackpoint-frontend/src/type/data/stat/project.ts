
/**
 * 项目统计中的单个项目
 */
export interface IProjectStat {
    id: string
    name: string
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
}

