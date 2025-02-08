import type { BaseResp } from "@/type/base";
import type { IUser, ReqLogin, ReqRegister, ReqUpdatePasswordByEmailCode, ReqUpdatePasswordByOri, ReqUpdateUserInfo } from "@/type/user";
import { request } from "@/util/request";


/**
 * 登录
 * @param data 
 * @returns 
 */
export function reqLogin(data: ReqLogin) {
    return request<ReqLogin, BaseResp<{ token: string }>>({
        url: '/user/login',
        method: 'post',
        data
    })
}



/**
 * 获取用户信息
 * @returns 
 */
export function reqUser() {
    return request<null, BaseResp<IUser>>({
        url: '/user',
        method: 'get',
    })
}



/**
 * 注册
 * @returns 
 */
export function reqRegister(data: ReqRegister) {
    return request<ReqRegister, BaseResp<{ token: string }>>({
        url: '/user/register',
        method: 'post',
        data
    })
}

/**
 * 发送邮箱验证码
 * @param data 
 * @returns 
 */
export function reqSendEmailCode(email: string) {
    return request<null, BaseResp<null>>({
        url: '/user/send-email-code',
        method: 'post',
        data: {
            email
        }
    })
}



/**
 * 使用邮箱验证码修改密码请求体
 * @param data
 * @returns 
 */
export function reqUpdatePasswordByEmailCode(data: ReqUpdatePasswordByEmailCode) {
    return request<ReqUpdatePasswordByEmailCode, BaseResp<null>>({
        url: '/user/updatepwd-email',
        method: 'put',
        data
    })
}


/**
 * 使用原密码修改密码请求体
 * @param data
 * @returns 
 */
export function reqUpdatePasswordByOri(data: ReqUpdatePasswordByOri) {
    return request<ReqUpdatePasswordByOri, BaseResp<null>>({
        url: '/user/updatepwd-pwd',
        method: 'put',
        data
    })
}


/**
 * 
 * @param data 修改用户信息，目前只考虑昵称
 * @returns 
 */
export function reqUpdateUserInfo(data: ReqUpdateUserInfo) {
    return request<ReqUpdatePasswordByEmailCode, BaseResp<null>>({
        url: '/user/info',
        method: 'put',
        data
    })
}


