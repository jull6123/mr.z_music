import { createRouter, createWebHistory } from 'vue-router'
import HelpView from '../views/HelpView.vue'
import PlayingView from '../views/PlayingView.vue'
import AiView from '@/views/AiView.vue'

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
      path: '/',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/registerView.vue')
    },
    {
      path: '/person',
      name: 'person',
      component: () => import('../views/personView.vue')
    },
    {
      path: '/auditHome',
      name: 'auditHome',
      component: () => import('../views/auditHomeView.vue')
    },
    {
      path: '/adminHome',
      name: 'adminHome',
      component: () => import('../views/adminHomeView.vue')
    },
    {
      path: '/home',
      name: 'home',
      component: () => import('../views/UserHome.vue')
    },
    {
      path: '/uploadPost',
      name: 'uploadPost',
      component: () => import('../views/uploadView.vue')
    },
  ]
})

export default router
