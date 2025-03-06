import { SideMenuPathEnum } from '@/enum'
import { goToPublicPage } from '@/util/goto'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: SideMenuPathEnum.Main,
      name: 'main',
      component: () => import('~dashboard/views/main/index.vue'),
      meta: {
        admin: true,
      },
    },
    {
      path: SideMenuPathEnum.ProjectOverview,
      name: 'project-overview',
      component: () => import('@/pages/dashboard/views/data/project-overview/index.vue'),
      meta: {
        admin: true,
      },
    },
    {
      path: SideMenuPathEnum.PerformanceMonitor,
      name: 'performance-monitor',
      component: () => import('~dashboard/views/data/performance-monitor/index.vue'),
      meta: {
        admin: true,
      },
    },
    {
      path: SideMenuPathEnum.UserAnalysis,
      name: 'user-analysis',
      component: () => import('~dashboard/views/data/user-analysis/index.vue'),
      meta: {
        admin: true,
      },
    },
    {
      path: SideMenuPathEnum.Project,
      name: 'project',
      component: () => import('~dashboard/views/project/index.vue'),
      meta: {
        admin: true,
      },
    },
    {
      path: SideMenuPathEnum.Event,
      name: 'event',
      component: () => import('~dashboard/views/event/index.vue'),
      meta: {
        admin: true,
      },
    },
    {
      path: SideMenuPathEnum.Record,
      name: 'record',
      component: () => import('~dashboard/views/record/index.vue'),
      meta: {
        admin: true,
      },
    },
    {
      path: SideMenuPathEnum.Test,
      name: 'test',
      component: () => import('~dashboard/views/test/index.vue'),
      meta: {
        admin: true,
      },
    },
  ],
})

router.beforeEach(async (to, from) => {
  // 去public，放行
  if (to.fullPath === '/') goToPublicPage()
  else return true
})

export default router
