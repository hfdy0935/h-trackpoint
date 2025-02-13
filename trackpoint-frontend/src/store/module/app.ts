import type { ThemeConfig } from 'ant-design-vue/es/config-provider/context'
import { computed, ref } from 'vue'
import { theme as theme_ } from 'ant-design-vue'
import { defineStore } from 'pinia'

function appStore() {
  const darkMode = ref<'dark' | 'light'>('light')
  const theme = computed<ThemeConfig>(() => ({
    algorithm: darkMode.value === 'light' ? theme_.defaultAlgorithm : theme_.darkAlgorithm,
  }))
  const bgColor = computed(() => (darkMode.value === 'dark' ? '#000' : '#fff'))
  const textColor = computed(() => (darkMode.value === 'dark' ? '#fff' : '#213547'))
  const toggleDarkMode = () => {
    darkMode.value = darkMode.value === 'light' ? 'dark' : 'light'
    document.documentElement.setAttribute('data-dark', darkMode.value)
  }
  return {
    darkMode,
    theme,
    bgColor,
    textColor,
    toggleDarkMode,
  }
}

export const useAppStore = defineStore('app', appStore, {
  persist: {
    pick: ['darkMode'],
  },
})
