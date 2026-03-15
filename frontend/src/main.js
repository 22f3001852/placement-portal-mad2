import { createApp } from 'vue'
import App from './App.vue'
import { router } from './router'

const app = createApp(App) // creates the root Vue app with App.vue as the root component
app.use(router) // after creating the app use router for routing
app.mount('#app') // mounts the Vue app to <div id="app"> in index.html

// createApp(App).use(router).mount("#app")