import { defineConfig } from "vite";
import tailwindcss from '@tailwindcss/vite'
import vue from "@vitejs/plugin-vue";
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
    base:
        mode == "development"
            ? "http://localhost:5173/"
            : "/static/api/spa/",
    build: {
        emptyOutDir: true,
        outDir: "../api/static/api/spa",
    },
    plugins: [vue(), tailwindcss(),],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
}));
