import path from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import frappeui from 'frappe-ui/vite'
import proxyOptions from "./proxyOptions";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [frappeui(), vue()],
  server: {
    port: 8080,
    proxy: proxyOptions,
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  build: {
    outDir: `../${path.basename(path.resolve('..'))}/public/frontend`,
    emptyOutDir: true,
    target: 'es2015',
  },
  optimizeDeps: {
    include: ['frappe-ui > feather-icons', 'showdown', 'engine.io-client'],
  },
})

// proxyOptions.ts
// const common_site_config = require("../../../sites/common_site_config.json");
// const { webserver_port } = common_site_config;

// export default {
//   "^/(app|api|assets|files|private)": {
//     target: `https://127.0.0.1:${webserver_port}`,
//     ws: true,
//     router: function (req) {
//       const site_name = req.headers.host.split(":")[0];
//       return `https://${site_name}`;
//     },
//   },
// };


// import { defineConfig } from 'vite'
// import vue from '@vitejs/plugin-vue'
// import path from 'path'
// import { getProxyOptions } from 'frappe-ui/src/utils/vite-dev-server'
// import { webserver_port } from '../../../sites/common_site_config.json'

// // https://vitejs.dev/config/
// export default defineConfig({
//   plugins: [vue()],
//   // server: {
//   //   port: 8080,
//   //   proxy: getProxyOptions({ port: webserver_port }),
//   // },
//   resolve: {
//     alias: {
//       '@': path.resolve(__dirname, 'src'),
//     },
//   },
//   build: {
//     outDir: `../${path.basename(path.resolve('..'))}/public/frontend`,
//     emptyOutDir: true,
//     target: 'es2015',
//   },
//   optimizeDeps: {
//     include: ['frappe-ui > feather-icons', 'showdown', 'engine.io-client'],
//   },
// })
