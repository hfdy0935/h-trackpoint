import { SideMenuEnum, SideMenuIcon, SideMenuNameEnum } from '@/enum'
import type { VNode } from 'vue'

export interface Item {
  key: string
  icon: string | VNode
  label: string
  name: string
  children?: Item[]
}
export const items: Item[] = [
  // key和path一样，不额外写字段了
  {
    key: SideMenuEnum.Main,
    icon: SideMenuIcon.Main,
    label: '首页',
    name: SideMenuNameEnum.Main,
  },
  {
    key: SideMenuEnum.Data,
    icon: SideMenuIcon.Data,
    label: '数据看板',
    name: '',
    children: [
      {
        key: SideMenuEnum.DataStatistic,
        icon: SideMenuIcon.DataStatistic,
        label: '数据统计',
        name: SideMenuNameEnum.DataStatistic,
      },
      {
        key: SideMenuEnum.PerformanceMonitor,
        icon: SideMenuIcon.PerformanceMonitor,
        label: '性能监控',
        name: SideMenuNameEnum.PerformanceMonitor,
      },
      {
        key: SideMenuEnum.MonitorAlert,
        icon: SideMenuIcon.MonitorAlert,
        label: '监控报警',
        name: SideMenuNameEnum.MonitorAlert,
      },
      {
        key: SideMenuEnum.UserBehaviorAnalysis,
        icon: SideMenuIcon.UserBehaviorAnalysis,
        label: '用户行为分析',
        name: SideMenuNameEnum.UserBehaviorAnalysis,
      },
    ],
  },
  {
    key: SideMenuEnum.Project,
    icon: SideMenuIcon.Project,
    label: '项目管理',
    name: SideMenuNameEnum.Project,
  },
  {
    key: SideMenuEnum.Event,
    icon: SideMenuIcon.Event,
    label: '事件管理',
    name: SideMenuNameEnum.Event,
  },
  {
    key: SideMenuEnum.Record,
    icon: SideMenuIcon.Record,
    label: '上报记录管理',
    name: SideMenuNameEnum.Record,
  },
  {
    key: SideMenuEnum.Test,
    icon: SideMenuIcon.Test,
    label: '调试',
    name: SideMenuNameEnum.Test,
  },
]

/**
 * 根据key/path找到item
 * @param key
 */
export function getItemByKey(items: Item[], key: string): Item | null {
  for (const item of items) {
    if (item.key === key) {
      return item
    }
    if (item.children) {
      const res = getItemByKey(item.children, key)
      if (res) return res
    }
  }
  return null
}
