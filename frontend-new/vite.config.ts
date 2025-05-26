import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    proxy: {
      '/api/v1': {
        target: 'http://api:8000',
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api\/v1/, '/api/v1'),
      },
    },
  },
});
