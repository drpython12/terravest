<template>
  <div class="min-h-screen bg-white flex flex-col items-center justify-center">
    <div class="w-full max-w-md px-6">
      <h1 class="text-5xl font-semibold text-center mb-12">Account</h1>
      <!-- Tabs -->
      <div class="flex justify-center mb-8 space-x-4">
        <button
          :class="{'border-b-4 border-blue-600 text-blue-600': tab === 'signup', 'text-gray-600': tab !== 'signup'}"
          class="pb-2 focus:outline-none"
          @click="tab = 'signup'"
        >
          Sign Up
        </button>
        <button
          :class="{'border-b-4 border-blue-600 text-blue-600': tab === 'login', 'text-gray-600': tab !== 'login'}"
          class="pb-2 focus:outline-none"
          @click="tab = 'login'"
        >
          Log In
        </button>
      </div>
      <!-- Form Card -->
      <div class="bg-gray-50 shadow-md rounded-lg p-8">
        <div v-if="tab === 'signup'">
          <h2 class="text-2xl font-medium mb-6 text-center">Create an Account</h2>
          <form @submit.prevent="submitSignup">
            <input
              type="text"
              placeholder="Username"
              v-model="signupData.username"
              class="w-full border border-gray-300 rounded p-3 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="email"
              placeholder="Email"
              v-model="signupData.email"
              class="w-full border border-gray-300 rounded p-3 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="password"
              placeholder="Password"
              v-model="signupData.password"
              class="w-full border border-gray-300 rounded p-3 mb-6 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="submit"
              class="w-full bg-blue-600 text-white py-3 rounded-full hover:bg-blue-700 transition-colors"
            >
              Sign Up
            </button>
          </form>
        </div>
        <div v-else-if="tab === 'login'">
          <h2 class="text-2xl font-medium mb-6 text-center">Log In</h2>
          <form @submit.prevent="submitLogin">
            <input
              type="email"
              placeholder="Email"
              v-model="loginData.email"
              class="w-full border border-gray-300 rounded p-3 mb-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <input
              type="password"
              placeholder="Password"
              v-model="loginData.password"
              class="w-full border border-gray-300 rounded p-3 mb-6 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="submit"
              class="w-full bg-blue-600 text-white py-3 rounded-full hover:bg-blue-700 transition-colors"
            >
              Log In
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Account',
  data() {
    return {
      tab: 'signup',
      signupData: {
        username: '',
        email: '',
        password: ''
      },
      loginData: {
        email: '',
        password: ''
      }
    };
  },
  methods: {
    submitSignup() {
      console.log('Sign Up Data:', this.signupData);
      // Insert your sign-up logic or API call here.
    },
    submitLogin() {
      console.log('Login Data:', this.loginData);
      // Insert your login logic or API call here.
    }
  }
});
</script>

<style scoped>
/* Additional custom styles if needed */
</style>
