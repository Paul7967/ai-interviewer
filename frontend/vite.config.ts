import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true, // Доступ с других устройств в сети
    proxy: {
      // Перенаправляем все запросы к /api на backend
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path,
        configure: (proxy, options) => {
          proxy.on('error', (err, req, res) => {
            console.log('proxy error', err);
          });
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('Sending Request to the Target:', req.method, req.url);
          });
          proxy.on('proxyRes', (proxyRes, req, res) => {
            console.log('Received Response from the Target:', proxyRes.statusCode, req.url);
          });
        },
      },
      // Также можно добавить proxy для OpenAPI схемы
      '/openapi.json': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      // И для документации API
      '/docs': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
      '/redoc': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
  // Оптимизация для продакшена
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          query: ['@tanstack/react-query'],
          ui: ['axios'],
        },
      },
    },
  },
  // Переменные окружения
  define: {
    __DEV__: JSON.stringify(process.env.NODE_ENV === 'development'),
  },
})
