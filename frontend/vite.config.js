import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  server:{
    host : '0.0.0.0',
    proxy: {
      '/api': {
        target: ' http://10.41.169.77:5000',
        changeOrigin: true,
        // No rewrite needed since Flask already expects /api prefix
      }
    }, 
    hmr: {
      protocol: 'ws',
      host: '10.41.169.77:5000', // Replace this with your actual local IP, e.g., '192.168.1.5'
      port: 5173
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
