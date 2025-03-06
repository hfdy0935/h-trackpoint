import '@/assets/main.css'

import { createApp } from 'vue'

import App from './App.vue'
import router from './router'
import pinia from '@/store'
import Antd from 'ant-design-vue'
import { sendClickEventDirective } from './directive'

const app = createApp(App)

app.use(pinia)
app.use(router).use(Antd)
app.directive('clickSend', sendClickEventDirective)
app.mount('#app')
