import { createApp, ref, reactive } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/css/vendor/bootstrap.min.css'
import './assets/css/minimal.css'
import './assets/css/vendor/jquery.mmenu.all.css'
import './assets/css/vendor/morris.css'
import './assets/css/vendor/rickshaw.min.css'
import 'element-plus/dist/index.css'
import ElementPlus from 'element-plus'
import prompt from './components/prompt/prompt.vue'
import headerbox from './components/headerbox/headerBox.vue'
import $ from 'jquery'

const app = createApp(App)
app.config.globalProperties.$usefake = ref(false)
app.config.globalProperties.$piesetting = reactive({ showall: false, showhis: false })
app.component('prompt', prompt)
app.component('header-box', headerbox)
app.use(router)
app.use(ElementPlus)
app.mount('#app')
