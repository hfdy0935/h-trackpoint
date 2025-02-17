import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { items } from '~dashboard/layout/component/side-menu/data'

export interface TagCacheItem {
  path: string // 路径
  name: string // 缓存的组件名，也作为SideMenuIconEnum中寻找图标的key
  label: string // 显示的文字
}
function dashboardStore() {
  const sideIds = ref<string[]>(['/dashboard/'])
  const collapsed = ref<boolean>(false) // 是否收起

  // tag缓存
  const tagCache = ref<TagCacheItem[]>([])
  const data = items[0]
  tagCache.value.push({
    ...data,
    path: '' + data.key,
  } as TagCacheItem)
  // 事件管理是否被缓存
  const isEventPageCached = computed<boolean>(() =>
    tagCache.value.some((item) => item.path === '/event'),
  )
  // 项目管理是否被缓存
  const isProjectPageCached = computed<boolean>(() =>
    tagCache.value.some((item) => item.path === '/project'),
  )

  return { sideIds, tagCache, collapsed, isEventPageCached, isProjectPageCached }
}

export const useDashboardStore = defineStore('dashboard', dashboardStore, {
  persist: true,
})
