import { reqEventList } from "@/api/v1/event";
import { DEFAULT_QUERY } from "@/constant";
import type { IProjectOption, ReqEventList, RespEventList } from "@/type/event";
import { ref } from "vue";
import { message } from 'ant-design-vue'
import { defineStore } from "pinia";
import { EventTypeEnum, StatusEnum } from "@/enum";
import { reqProjectOptions } from "@/api/v1/project";
/**
 * 过滤事件的方式
 */
export type FilterEventField = 'create_time' | 'update_time' | 'project_num'
function eventStore() {
    // 查询数据
    const query = ref<ReqEventList>({ type: EventTypeEnum.DEFAULT, status: [StatusEnum.NORMAL, StatusEnum.DISABLED], page: DEFAULT_QUERY })
    // 点击表格过滤时的字段名
    const filterEventField = ref<FilterEventField>('create_time')
    // 默认事件列表
    const defaultData = ref<RespEventList>({} as RespEventList)
    // 自定义事件列表
    const customData = ref<RespEventList>({} as RespEventList)
    /**
     * 更新事件列表
     */
    const refresh = async () => {
        try {
            // 根据项目名列表找到对应的项目id列表
            const resp = await reqEventList({
                ...query.value,
                projectIdList: query.value.projectIdList?.map(el => projectOptions.value.find(el1 => el1.name === el)!.id)
            })
            if (resp.code === 200) {
                if (query.value.type === EventTypeEnum.DEFAULT) defaultData.value = resp.data
                else customData.value = resp.data
            }
            else message.error(resp.msg)
        } catch {
            message.error('获取事件失败')
        }
        try {
            const resp = await reqProjectOptions()
            if (resp.code === 200) projectOptions.value = resp.data
        } catch { }
    }
    // 项目选项，用于创建/修改事件时选择
    const projectOptions = ref<IProjectOption[]>([])

    return { query, filterEventField, defaultData, customData, refresh, projectOptions }
}



export const useEventStore = defineStore('eventStore', eventStore)