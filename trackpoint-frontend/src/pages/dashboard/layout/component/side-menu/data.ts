import { SideMenuPathEnum, SideMenuIcon, SideMenuNameEnum } from '@/enum'
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
    key: SideMenuPathEnum.Main,
    icon: SideMenuIcon.Main,
    label: '首页',
    name: SideMenuNameEnum.Main,
  },
  {
    key: SideMenuPathEnum.Data,
    icon: SideMenuIcon.Data,
    label: '数据看板',
    name: '',
    children: [
      {
        key: SideMenuPathEnum.ProjectOverview,
        icon: SideMenuIcon.ProjectOverview,
        label: '项目总览',
        name: SideMenuNameEnum.ProjectOverview,
      },
      {
        key: SideMenuPathEnum.PerformanceMonitor,
        icon: SideMenuIcon.PerformanceMonitor,
        label: '性能监控',
        name: SideMenuNameEnum.PerformanceMonitor,
      },
      {
        key: SideMenuPathEnum.UserAnalysis,
        icon: SideMenuIcon.UserAnalysis,
        label: '用户分析',
        name: SideMenuNameEnum.UserAnalysis,
      },
    ],
  },
  {
    key: SideMenuPathEnum.Project,
    icon: SideMenuIcon.Project,
    label: '项目管理',
    name: SideMenuNameEnum.Project,
  },
  {
    key: SideMenuPathEnum.Event,
    icon: SideMenuIcon.Event,
    label: '事件管理',
    name: SideMenuNameEnum.Event,
  },
  {
    key: SideMenuPathEnum.Record,
    icon: SideMenuIcon.Record,
    label: '上报记录管理',
    name: SideMenuNameEnum.Record,
  },
  {
    key: SideMenuPathEnum.Test,
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
