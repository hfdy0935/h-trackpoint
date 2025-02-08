import { useLocalStorage } from "@vueuse/core"
import { computed } from "vue"

interface AppStoreLocalStorageData {
    darkMode: 'light' | 'dark'
}
export default function useTheme() {
    // 无法直接使用pinia中的变量
    const app = useLocalStorage<AppStoreLocalStorageData>('app', (JSON.parse(localStorage.getItem('app') ?? '{}')))
    const bgColor = computed(() => app.value.darkMode === 'dark' ? '#000' : '#fff')
    const textColor = computed(() => app.value.darkMode === 'dark' ? '#fff' : '#213547')
    return {
        bgColor, textColor
    }
}