<template>
  <div class="container">
    <h2 class="title">Account Settings</h2>
    <form @submit.prevent="updateSettings">
      <div class="input-container">
        <label for="firstName">First Name</label>
        <input v-model="firstName" id="firstName" type="text" class="input-box" />
      </div>
      <div class="input-container">
        <label for="lastName">Last Name</label>
        <input v-model="lastName" id="lastName" type="text" class="input-box" />
      </div>
      <div class="input-container">
        <label for="email">Email</label>
        <input v-model="email" id="email" type="email" class="input-box" />
      </div>
      <button type="submit" class="submit-button">Update Settings</button>
    </form>
  </div>
</template>

<script>
import axiosInstance from '../axiosConfig';
import { useAuthStore } from '../store/useAuthStore';

export default {
  name: 'AccountSettingsPage',
  data() {
    return {
      firstName: '',
      lastName: '',
      email: '',
    };
  },
  async created() {
    const authStore = useAuthStore();
    await authStore.fetchUser();
    const user = authStore.user;
    if (user) {
      this.firstName = user.first_name;
      this.lastName = user.last_name;
      this.email = user.email;
    }
  },
  methods: {
    async updateSettings() {
      try {
        const response = await axiosInstance.post('/account/update-settings/', {
          first_name: this.firstName,
          last_name: this.lastName,
          email: this.email,
        });
        if (response.data.success) {
          alert('Settings updated successfully!');
        }
      } catch (error) {
        console.error('Settings update error:', error);
      }
    },
  },
};
</script>

<style scoped>
/* Container styling */
.container {
  text-align: center;
  background: white;
  padding: 40px;
  border-radius: 10px;
  width: 500px;
  margin: auto;
  margin-top: 50px;
}

/* Title styling */
.title {
  font-size: 22px;
  font-weight: bold;
  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue", Helvetica, Arial, sans-serif;
  margin-bottom: 20px;
}

/* Input box styling */
.input-box {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  outline: none;
  margin-bottom: 10px;
}

/* Submit button styling */
.submit-button {
  background-color: #007aff;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
}

.submit-button:hover {
  background-color: #005bb5;
}
</style>