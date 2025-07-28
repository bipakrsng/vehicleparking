// import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router/router'
import NavBar from './components/NavBar.vue'
import {createPinia} from 'pinia'
import { useUserStore } from './store/userStore'
import { decodeToken } from '@/utils/auth'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)

// Registering the NavBar component globally

app.component('nav-bar',NavBar)
app.use(router)

const userStore = useUserStore();
const token = decodeToken();
if (token){
    userStore.setUserFromToken(token);
}

app.mount('#app');
