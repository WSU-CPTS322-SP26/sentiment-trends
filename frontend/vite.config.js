import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
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
  },
});
