import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";
import tailwindcss from '@tailwindcss/vite'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
  base: mode === "development" ? "/" : "/static/api/spa/",
  build: {
    emptyOutDir: true,
    outDir: "../api/static/api/spa",
  },
  plugins: [vue(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `
          @import "@/assets/scss/_variables.scss";`,
      },
    },
  },
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000", // Backend server
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, "/api"), // Keep the /api prefix
      },
    },
  },
}));
