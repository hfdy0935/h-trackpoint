import type { PageQuery } from "@/type/base"

/**
 * 邮件验证码发送时间间隔，2min
 */
export const EMAIL_CODE_EXPIRATION_TIME = 2 * 60


/**
 * 默认分页查询参数
 */
export const DEFAULT_PAGE_QUERY: PageQuery = {
    pageNum: 1,
    pageSize: 10
}