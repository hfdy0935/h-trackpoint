import { reqUser } from '@/api/v1/user'
import { useUserStore } from '@/store'
import { goToDashBoard } from '@/util/goto'
import { storeToRefs } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import { message } from 'ant-design-vue'
import { SideMenuPathEnum, SideMenuNameEnum, type SideMenuKey } from '@/enum'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: () => import('~site/views/main/index.vue'),
      meta: {
        public: true
      }
    },
    ...Object.entries(SideMenuPathEnum).map(([k, v]) => ({
      path: v,
      name: SideMenuNameEnum[k as SideMenuKey],
      component: () => import('~site/views/main/index.vue'),
    }))
  ],
})

router.beforeEach(async (to) => {
  if (to.meta.public) {
    return true
  } else {
    const { modalShow, token } = storeToRefs(useUserStore())
    // 先判断token
    if (!token.value) {
      message.warning('请先登录')
      modalShow.value = true
      return false
    }
    else {
      reqUser().then(res => {
        if (res.code === 200) {
          message.success('登录成功')
          goToDashBoard(1000)
        } else {
          message.warning('登录已过期或未登录')
          modalShow.value = true
          return '/'
        }
      }).catch(() => {
        message.warning('请先登录')
        modalShow.value = true
        return '/'
      })
    }
  }
})



export default router
