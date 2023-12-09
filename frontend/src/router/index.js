import { createRouter, createWebHistory } from 'vue-router'
import AllStatus from '../views/AllStatus.vue'
import Login from '../views/authentication/Login.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'allStatus',
      component: AllStatus
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    }
  ]
})

export default router
