import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { IUser } from '@/type/user'
import { goToPublicPage } from '@/util/goto'
import { message } from 'ant-design-vue'
import { reqUser } from '@/api/v1/user'
import { AccountOpEnum } from '@/enum'

function userStore() {
  const user = ref<IUser>({} as IUser)
  const clear = () => {
    user.value = {} as IUser
  }
  const token = ref('')

  /**
   * 刷新用户信息，比如创建项目之后
   */
  const refresh = async () => {
    try {
      const resp = await reqUser()
      if (resp.code === 200) user.value = resp.data
    } catch {}
  }
  const logout = (showTip: boolean = true) => {
    user.value = {} as IUser
    token.value = ''
    showTip && message.success('退出成功')
    goToPublicPage(500)
  }

  const publicTabKey = ref<string[]>(['/']) // 主页tab激活的key
  const modalShow = ref(false) // 登录注册改密码的对话框
  const op = ref<AccountOpEnum>(AccountOpEnum.LOGIN) // 登陆注册找回密码对话框显示什么
  return { user, clear, token, refresh, logout, publicTabKey, modalShow, op }
}

export const useUserStore = defineStore('user', userStore, {
  persist: {
    pick: ['token'],
  },
})
