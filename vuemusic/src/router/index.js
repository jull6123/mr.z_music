import { createRouter, createWebHistory } from 'vue-router'
import HelpView from '../views/HelpView.vue'
import PlayingView from '../views/PlayingView.vue'
import AiView from '@/views/AiView.vue'
import TestView from "@/views/TestView.vue";

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
      path: '/test',
      name: 'test',
      component: TestView
    },
  ]
})

export default router
