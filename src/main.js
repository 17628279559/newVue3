import { createApp } from 'vue'
import App from './App.vue'
import './assets/css/vendor/bootstrap.min.css'
import './assets/css/minimal.css'
import './assets/css/vendor/jquery.mmenu.all.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
app.use(ElementPlus)
app.mount('#app')
