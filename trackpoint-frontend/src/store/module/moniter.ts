import { defineStore } from 'pinia'
import { getMonitorOverview, getJsErrors } from '@/api/v1/monitor'

interface MonitorState {
  overview: {
    healthStatus: number
    jsErrorRatio: number
    // ...其他字段
  }
  jsErrors: JsError[]
  loading: boolean
  lastUpdated: Date | null
}

export const useMonitorStore = defineStore('monitor', {
  state: (): MonitorState => ({
    overview: {
        /* 初始化字段 */
        healthStatus: 0,
        jsErrorRatio: 0

    },
    jsErrors: [],
    loading: false,
    lastUpdated: null
  }),
  actions: {
    async fetchAll() {
      try {
        this.loading = true
        await Promise.all([
          this.fetchOverview(),
          this.fetchJsErrors()
        ])
        this.lastUpdated = new Date()
      } finally {
        this.loading = false
      }
    },
    async fetchOverview() {
      const { data } = await getMonitorOverview()
      this.overview = data
    },
    async fetchJsErrors() {
      const { data } = await getJsErrors()
      this.jsErrors = data.list
    }
  },
  getters: {
    formattedTrend: (state) => {
      return state.overview.jsErrorTrend.map(([time, value]) => ({
        time: new Date(time).toLocaleTimeString(),
        value
      }))
    }
  }
})