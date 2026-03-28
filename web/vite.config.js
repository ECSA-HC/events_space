import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path' // 👈 make sure to import path

export default defineConfig({
  plugins: [vue()],
  server: {
    host: true,   // expose on LAN (0.0.0.0) so phones can reach it
    port: 5174,
    proxy: {
      // All /api/* requests are forwarded to the FastAPI backend.
      // This eliminates CORS entirely — the browser only ever talks to Vite.
      '/api': {
        target: 'http://localhost:8002',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'), // 👈 alias for @
    },
  },
})
