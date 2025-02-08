import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'
import { resolve } from 'node:path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), vueJsx(), vueDevTools()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '~site': fileURLToPath(new URL('./src/pages/site', import.meta.url)),
      '~dashboard': fileURLToPath(new URL('./src/pages/dashboard', import.meta.url)),
    },
  },
  build: {
    rollupOptions: {
      input: {
        main: resolve(__filename, './index.html'),
        dashboard: resolve(__filename, './dashboard/index.html'),
        sdkTest: resolve(__filename, './sdk-test/index.html')
      },
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api/, '')
      }
    }
  }
})
