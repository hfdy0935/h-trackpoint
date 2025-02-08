import '@/assets/main.css'

import { createApp } from 'vue'

import App from './App.vue'
import Antd from 'ant-design-vue'
import pinia from '@/store'

const app = createApp(App)

app.use(Antd).use(pinia)

app.mount('#app')
