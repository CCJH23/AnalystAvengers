// import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'

// const router = createRouter({
//   history: createWebHistory(import.meta.env.BASE_URL),
//   routes: [
//     {
//       path: '/',
//       name: 'home',
//       component: HomeView
//     },
//     {
//       path: '/about',
//       name: 'about',
//       // route level code-splitting
//       // this generates a separate chunk (About.[hash].js) for this route
//       // which is lazy-loaded when the route is visited.
//       component: () => import('../views/AboutView.vue')
//     }
//   ]
// })

// export default router

import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import ViewAllView from '../views/ViewAllView.vue';
import ViewEachView from '../views/ViewEachView.vue'
import TopNavbar from '@/components/Navbar/TopNavbar.vue';
import Sidebar from '@/components/Navbar/Sidebar.vue';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/viewall',
      name: 'viewall',
      component: ViewAllView,
    },
    {
      path: '/vieweach',
      name: 'vieweach',
      component: ViewEachView,
    },
    {
      // Redirect any unknown routes to the login page
      path: '/:catchAll(.*)',
      redirect: '/login',
    },
  ],
});

export default router;
export const components = {
  TopNavbar,
};