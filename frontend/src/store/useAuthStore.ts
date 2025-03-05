import { defineStore } from 'pinia';
import axiosInstance from '../axiosConfig';
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isLoggedIn: false,
    user: null,
  }),
  actions: {
    async fetchUser() {
      try {
        const response = await axiosInstance.get('/api/app-data');
        this.isLoggedIn = response.data.isLoggedIn;
        this.user = response.data.user;
      } catch (error) {
        console.error(error);
      }
    },
    async login(email, password) {
      try {
        const response = await axiosInstance.post('/account/login/', { email, password });
        if (response.data.success) {
          this.isLoggedIn = true;
          this.user = response.data.user;
          return response.data.redirect;
        }
      } catch (error) {
        console.error(error);
        throw error;
      }
    },
    async logout() {
      try {
        await axiosInstance.post('/account/logout/');
        this.isLoggedIn = false;
        this.user = null;
        const router = useRouter();
        router.push('/login');
      } catch (error) {
        console.error(error);
      }
    },
  },
});