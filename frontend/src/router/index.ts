import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '@/pages/MainPage.vue';
import AccountPage from '@/pages/AccountPage.vue';
import SignupPage from '@/pages/SignupPage.vue';
import LoginPage from '@/pages/LoginPage.vue';
import PreferencesPage from '@/pages/PreferencesPage.vue';
import DashboardPage from '@/pages/DashboardPage.vue';
import AccountSettingsPage from '@/pages/AccountSettingsPage.vue';
import PortfolioPage from '@/pages/PortfolioPage.vue';

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
    component: SignupPage,
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage,
  },
  {
    path: '/account/preferences',
    name: 'PreferencesPage',
    component: PreferencesPage,
  },
  {
    path: '/dashboard',
    name: 'DashboardPage',
    component: DashboardPage,
  },
  {
    path: '/account/settings',
    name: 'SettingsPage',
    component: AccountSettingsPage,
  },
  {
    path: '/account/portfolio',
    name: 'PortfolioPage',
    component: PortfolioPage,
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;