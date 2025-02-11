import { DEFAULT_PAGE_QUERY } from '@/constant'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ReqRecordList, RespProjectEventInfo, RespRecordList } from '@/type/record'
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
  const respProjEventOptions = ref<RespProjectEventInfo[]>([])
  const refresh = async () => {
    try {
      // 根据项目/事件名找到项目/事件id
      const selectedProject = respProjEventOptions.value.find(
        (p) => p.project_name === query.value.projectId,
      )
      const projectId = selectedProject?.project_id
      const eventId = selectedProject?.events.find(
        (e) => e.event_name === query.value.eventId,
      )?.event_id
      // 两个都选了才发送请求获取上报记录
      if (projectId && eventId) {
        const resp = await reqRecordList({
          ...query.value,
          projectId,
          eventId,
        })
        if (resp.code === 200) {
          message.success('查询上报记录成功')
          data.value = resp.data
        } else message.error(resp.msg)
      } else {
        // 否则清空原数据
        resetData()
      }
    } catch {
      message.error('获取上报记录失败')
    }
  }
  return { query, data, resetData, respProjEventOptions, refresh }
}

export const useRecordStore = defineStore('record', recordStore)
