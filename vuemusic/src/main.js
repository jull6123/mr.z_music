import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import './assets/gloable.css'



const app = createApp(App)
for (const [name, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(name, component);
}
app.config.globalProperties.$currentIndex = -1;
app.config.globalProperties.$MusicUrl = '1111111111';

app.config.globalProperties.$setMusicUrl = function(value) {
    app.config.globalProperties.$MusicUrl = value;
};
app.use(createPinia())
app.use(router)
app.use(ElementPlus)
app.mount('#app')


