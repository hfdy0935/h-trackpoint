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
 * 基本信息的响应体
 */
export interface RespBaseStat {
    // /**
    //  * 项目数量
    //  */
    // project_num: number
    // /**
    //  * 事件数量
    //  */
    // event_num: number
    /**
     * 客户端列表
     */
    client_list: IClient[]
}