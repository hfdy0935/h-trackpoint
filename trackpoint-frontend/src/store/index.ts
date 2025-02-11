import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

export { useUserStore } from './module/user';
export { useAppStore } from './module/app'
export { useDashboardStore } from './module/dashboard';
export { useProjectStore } from './module/project'
export { useEventStore } from './module/event'
export {useRecordStore} from './module/record'


const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
export default pinia