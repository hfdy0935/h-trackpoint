/**
 * 基本响应体
 */
export interface BaseResp<T> {
    code: number
    msg: string
    data: T
}

/**
 * 分页查询请求体的页码部分
 */
export interface PageQuery {
    pageNum: number
    pageSize: number
}


/**
 * 分页查询结果
 */
export interface PageVO<T> {
    page_num: number
    page_size: number
    total: number
    records: T[]
}


/**
 * 查询时字段排序
 */
export interface OrderBy {
    field?: string
    order?: 'ascend' | 'descend'
}



/**
 * 查询时时间范围
 */
export interface TimePeriod {
    start?: string
    end?: string
}