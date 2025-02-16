import { reqProjectList } from "@/api/v1/project"
import { DEFAULT_PAGE_QUERY } from "@/constant"
import type { ReqProjectList, RespEventOpions, RespProjectList } from "@/type/project"
import { defineStore } from "pinia"
import { ref } from "vue"
import { message } from "ant-design-vue"
import { StatusEnum } from "@/enum"
import { reqEventOptions } from "@/api/v1/event"


export type FilterProjectField = 'create_time' | 'update_time' | 'event_num'
function projectStore() {
    // 查询数据
    const query = ref<ReqProjectList>({ status: [StatusEnum.NORMAL, StatusEnum.DISABLED], page: DEFAULT_PAGE_QUERY })
    // 点击表格过滤时的字段名
    const filterProjectField = ref<FilterProjectField>('create_time')
    // 项目列表响应体
    const data = ref<RespProjectList>({} as RespProjectList)
    /**
     * 更新项目列表
     */
    const refresh = async () => {
        try {
            const resp = await reqProjectList(query.value)
            if (resp.code === 200) data.value = resp.data
            else message.error(resp.msg)
        } catch {
            message.error('获取项目失败')
        }
        try {
            const resp = await reqEventOptions()
            if (resp.code === 200) eventOptions.value = resp.data
        } catch { }
    }
    // 事件选项，用于创建/修改项目时选择
    const eventOptions = ref<RespEventOpions>({ default: [], custom: [] })
    return { query, filterProjectField, data, refresh, eventOptions, }
}


export const useProjectStore = defineStore('project', projectStore)