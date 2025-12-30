import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: parseInt(process.env.VITE_PORT || '3000'),
    proxy: {
      '/expense': 'http://localhost:8000',
      '/income': 'http://localhost:8000',
      '/purpose': 'http://localhost:8000',
      '/ledger': 'http://localhost:8000',
      '/report': 'http://localhost:8000',
      '/insights': 'http://localhost:8000',
      '/signup': 'http://localhost:8000',
      '/signin': 'http://localhost:8000'
    }
  }
})
