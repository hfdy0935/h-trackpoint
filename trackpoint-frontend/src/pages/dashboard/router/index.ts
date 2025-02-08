import { goToPublicPage } from '@/util/goto'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/dashboard',
      name: 'main',
      component: () => import('~dashboard/views/main/index.vue'),
      meta: {
        admin: true
      }
    },
    {
      path: '/data-statistic',
      name: 'data-statistic',
      component: () => import('~dashboard/views/data/data-statistic/index.vue'),
      meta: {
        admin: true
      }
    },
    {
      path: '/performance-monitor',
      name: 'performance-monitor',
      component: () => import('~dashboard/views/data/performance-monitor/index.vue'),
      meta: {
        admin: true
      }
    },
    {
      path: '/monitor-alert',
      name: 'monitor-alert',
      component: () => import('~dashboard/views/data/monitor-alert/index.vue'),
      meta: {
        admin: true
      }
    },
    {
      path: '/user-behavior-analysis',
      name: 'user-behavior-analysis',
      component: () => import('~dashboard/views/data/user-behavior-analysis/index.vue'),
      meta: {
        admin: true
      }
    },
    {
      path: '/project',
      name: 'project',
      component: () => import('~dashboard/views/project/index.vue'),
      meta: {
        admin: true
      }
    },
    {
      path: '/event',
      name: 'event',
      component: () => import('~dashboard/views/event/index.vue'),
      meta: {
        admin: true
      }
    },
    {
      path: '/test',
      name: 'test',
      component: () => import('~dashboard/views/test/index.vue'),
      meta: {
        admin: true
      }
    },
  ],
})


router.beforeEach(async (to, from) => {
  // 去public，放行
  if (to.fullPath === '/') goToPublicPage()
  else return true
})

export default router
