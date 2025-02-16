import { request } from '@/utils/request'


export interface JsError {
    time: string
    count: number
    pageUrl: string
    reason: string
}

export interface RequestError {
    time: string
    count: number
    statusCode: number
    method: string
}

export const getJsErrors = () => {
    return request.get<JsError[]>('/monitor/js-errors')
}

export const getRequestErrors = () => {
    return request.get<RequestError[]>('/monitor/request-errors')
}

