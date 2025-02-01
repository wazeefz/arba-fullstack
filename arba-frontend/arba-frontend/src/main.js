/**
 * main.js
 *
 * Bootstraps Vuetify, Pinia, and other plugins, then mounts the App
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Pinia for global state management
import { createPinia } from 'pinia'

const app = createApp(App)

// Register Pinia store
app.use(createPinia()) // <-- Use Pinia here

// Register other plugins
registerPlugins(app)

// Mount the app
app.mount('#app')
