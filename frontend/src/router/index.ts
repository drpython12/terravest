import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '@/pages/MainPage.vue';
import AccountPage from '@/pages/AccountPage.vue';
import SignUpPage from '../pages/SignupPage.vue';

const routes = [
  {
    path: '/',
    name: 'MainPage',
    component: MainPage,
  },
  {
    path: '/account',
    name: 'AccountPage',
    component: AccountPage,
  },
  { 
    path: '/signup', 
    name: 'SignupPage',
    component: SignUpPage,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;