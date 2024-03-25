import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import DashboardView from '../views/DashboardView.vue';
import sockettest from '../views/sockettest.vue';
import ViewEachServerView from "../views/ViewEachServerView.vue";
import alertsockettest from "../views/alertsockettest.vue";
import ViewServiceGroup from '../views/ViewServiceGroup.vue'
import ViewAllView from '../views/ViewAllView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'viewall',
      component: ViewAllView,
    },
    {
      path: '/view/:serviceGroup',
      name: 'view',
      component: ViewServiceGroup
    },
    {
      path: '/vieweachserver/:infrastructureName',
      name: 'ViewEachServer',
      component: ViewEachServerView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
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
      path: '/sockettest',
      name: 'sockettest',
      component: sockettest,
    },
    {
      path: '/alertsockettest',
      name: 'alertsockettest',
      component: alertsockettest,
    },
    {
      // Redirect any unknown routes to the login page
      path: '/:catchAll(.*)',
      redirect: '/login',
    },
  ],
});

export default router;