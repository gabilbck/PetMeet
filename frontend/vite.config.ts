import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// O front fala com a API por /api. Em desenvolvimento o proxy abaixo evita
// qualquer questao de CORS; em producao aponte VITE_API_URL para a API real.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (caminho) => caminho.replace(/^\/api/, ''),
      },
      '/uploads': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
