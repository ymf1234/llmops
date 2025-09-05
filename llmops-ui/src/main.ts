import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ArcoVue from '@arco-design/web-vue'
// 额外引入图标库
import ArcoVueIcon from '@arco-design/web-vue/es/icon'

import App from '@/App.vue'
import router from '@/router'

import '@arco-design/web-vue/dist/arco.css'
import '@/assets/styles/main.css'
// import '@/assets/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ArcoVue)
app.use(ArcoVueIcon)

app.mount('#app')
