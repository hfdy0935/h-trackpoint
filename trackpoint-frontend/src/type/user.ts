/**
 * 用户登录请求体
 */
export interface ReqLogin {
    email: string
    password: string
}

/**
 * 用户信息
 */
export interface IUser {
    id: string
    email: string
    nickname: string
    createTime: string
    /**
     * 项目数量限制
     */
    projectNumLimit: number
    /**
     * 单个项目最大添加事件数量限制
     */
    eventNumLimit: number
    /**
     * 项目数量
     */
    projectNum: number
    /**
     * 事件数量
     */
    eventNum: number
}


/**
 * 注册请求体
 */
export interface ReqRegister extends ReqLogin {
    /**
     * 昵称
     */
    nickname?: string
    /**
     * 邮箱验证码
     */
    code: string
}


/**
 * 用邮箱验证码修改密码请求体
 */
export type ReqUpdatePasswordByEmailCode = Omit<ReqRegister, 'nickname'>



/**
 * 修改用户信息请求体
 */
export interface ReqUpdateUserInfo {
    nickname: string
}


/**
 * 用原密码修改密码请求体
 */
export interface ReqUpdatePasswordByOri {
    oriPassword: string
    newPassword: string
}