import type { BaseResp } from "@/type/base";
import type { IProjectOption } from "@/type/event";
import type { ReqCreateProject, ReqProjectList, ReqUpdateProject, ReqUpdateProjectStatus, RespCreateProject, RespProjectList } from "@/type/project";
import { request } from "@/util/request";


/**
 * 获取项目选项，用于创建/修改事件时选
 * @returns 
 */
export function reqProjectOptions() {
    return request<undefined, BaseResp<IProjectOption[]>>({
        url: '/project/option',
        method: 'get',
    })
}

/**
 * 
 * @param data 获取项目列表
 * @returns 
 */
export function reqProjectList(data: ReqProjectList) {
    return request<ReqProjectList, BaseResp<RespProjectList>>({
        url: '/project/list',
        method: 'post',
        data
    })
}

/**
 * 创建项目
 * @param data 
 * @returns 
 */
export function reqCreateProject(data: ReqCreateProject) {
    return request<ReqCreateProject, BaseResp<RespCreateProject>>({
        url: '/project',
        method: 'post',
        data
    })
}

/**
 * 删除项目
 * @param id 项目id 
 * @returns 
 */
export function reqDeleteProject(id: string) {
    return request<string, BaseResp<null>>({
        url: `/project/${id}`,
        method: 'delete',
    })
}

/**
 * 修改项目
 * @param data 
 * @returns 
 */
export function reqUpdateProject(data: ReqUpdateProject) {
    return request<ReqUpdateProject, BaseResp<null>>({
        url: '/project',
        method: 'put',
        data
    })
}

/**
 * 修改项目状态
 * @param data 
 * @returns 
 */
export function reqUpdateProjectStatus(data: ReqUpdateProjectStatus) {
    return request<ReqUpdateProject, BaseResp<null>>({
        url: '/project/status',
        method: 'put',
        data
    })
}

