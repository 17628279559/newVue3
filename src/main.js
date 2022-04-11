import { createApp } from 'vue'
import App from './App.vue'
import './assets/css/vendor/bootstrap.min.css'
import './assets/css/minimal.css'
import './assets/css/vendor/jquery.mmenu.all.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import $ from 'jquery'

const app = createApp(App)
app.config.globalProperties.$usefake = false
app.use(ElementPlus)
app.mount('#app')
