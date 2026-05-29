import { createApp, h, Suspense } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import './main.css'

const app = createApp({
    render: () => h(Suspense, null, { default: () => h(App) })
})

app.use(createPinia())
app.use(router)

app.mount('#app')
