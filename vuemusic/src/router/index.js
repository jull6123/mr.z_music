import { createRouter, createWebHistory } from 'vue-router'
import HelpView from '../views/HelpView.vue'
import PlayingView from '../views/PlayingView.vue'
import AiView from '@/views/AiView.vue'
import personView from "@/views/personView.vue";
import LoginView from "@/views/LoginView.vue";
import registerView from "@/views/registerView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/help',
      name: 'help',
      component: HelpView
    },
    {
      path: '/playing',
      name: 'Playing',
      component: PlayingView
    },
    {
      path:'/ai',
      name:'Ai',
      component:AiView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: registerView
    },
    {
      path: '/person',
      name: 'person',
      component: personView
    },
  ]
})

export default router
