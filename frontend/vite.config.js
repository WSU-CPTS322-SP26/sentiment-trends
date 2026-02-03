import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5001,
    watch: {
      usePolling: true,
    },
    hmr: {
      host: "localhost",
      port: 5001,
    },
    proxy: {
      "/api": {
        target: "http://backend:3001",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
