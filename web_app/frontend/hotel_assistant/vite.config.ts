import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Allow access to node_modules directory
    fs: {
      allow: [
        // Allow project root directory
        path.resolve(__dirname),
        // Allow node_modules directory
        path.resolve(__dirname, '../node_modules'),
        // Allow parent node_modules directory
        path.resolve(__dirname, '../../node_modules')
      ]
    },
    // Configure API proxy to avoid CORS issues
    proxy: {
      '/api': {
        target: 'http://0.0.0.0:9871',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
