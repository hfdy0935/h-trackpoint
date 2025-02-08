import path, { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { defineConfig } from "vite";

const __dirname = dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  build: {
    lib: {
      entry: resolve(__dirname, "lib/main.ts"),
      name: "h-trackpoint",
    },
    rollupOptions: {
      external: ["axios", "ua-parser-js", "@types/node", "html2canvas"], // 排除，不打包进本项目
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "lib"),
    },
  },
});
