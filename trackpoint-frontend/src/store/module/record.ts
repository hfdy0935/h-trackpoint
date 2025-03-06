import { DEFAULT_PAGE_QUERY } from '@/constant'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ReqRecordList, IProjectEventInfo, RespRecordList } from '@/type/record'
import { reqRecordList } from '@/api/v1/record'
import { message } from 'ant-design-vue'

function recordStore() {
  // 查询数据
  const query = ref<ReqRecordList>({
    projectId: '',
    eventId: '',
    page: DEFAULT_PAGE_QUERY,
    filterParamList: [],
  } as ReqRecordList)
  // 上报记录列表响应体a
  const data = ref<RespRecordList>({} as RespRecordList)
  const resetData = () => {
    data.value = {} as RespRecordList
  }
  // 各项目下事件选项响应体
  const respProjEventOptions = ref<IProjectEventInfo[]>([])
  const refresh = async () => {
    if (!query.value.projectId || !query.value.eventId) {
      data.value = {} as RespRecordList
      return
    }
    try {
      const resp = await reqRecordList({
        ...query.value,
        orderBy: query.value.orderBy?.filter((o) => o.field && o.order),
      })
      if (resp.code === 200) {
        data.value = resp.data
      } else message.error(resp.msg)
    } catch {
      message.error('获取上报记录失败')
    }
  }
  return { query, data, resetData, respProjEventOptions, refresh }
}

export const useRecordStore = defineStore('record', recordStore)
