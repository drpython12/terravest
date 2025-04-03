<template>
  <div class="container">
    <h2 class="title">Sign in to the TerraVest Portal</h2>
    
    <!-- Email input with arrow -->
    <div class="input-container">
      <input 
        v-model="email" 
        type="text" 
        class="input-box" 
        placeholder="Email or Phone Number" 
        @blur="validateEmail"
        aria-label="Email or Phone Number"
      />
      <span v-if="showEmailArrow" class="arrow-icon" @click="checkUserExists">➜</span>
    </div>
    <p v-if="emailError" class="error-message">⚠ Please enter a valid email address.</p>
    <p v-if="userNotFoundError" class="error-message">⚠ This email is not registered. <router-link to="/signup">Sign up now.</router-link></p>

    <!-- Password input with arrow -->
    <div class="input-container" v-if="showPassword">
      <input 
        v-model="password" 
        type="password" 
        class="input-box" 
        placeholder="Password"
        @blur="validatePassword"
        aria-label="Password"
      />
      <span v-if="showPasswordArrow" class="arrow-icon" @click="loginUser">➜</span>
    </div>
    <p v-if="passwordError" class="error-message">⚠ Password must be entered.</p>
    <p v-if="loginError" class="error-message">⚠ {{ loginError }}</p>
    <p v-if="successMessage" class="success-message">🎉 {{ successMessage }}</p>

    <div class="remember-me">
      <input type="checkbox" id="remember" v-model="rememberMe" />
      <label for="remember">&nbsp;&nbsp;Remember me</label>
    </div>
    <div class="links">
      <a href="#">Forgotten your password?</a><br />
      <span>Do not have a TerraVest Account? <router-link to="/signup">Create yours now.</router-link></span>
    </div>
  </div>
</template>

<script>
import axiosInstance from '../axiosConfig';
import { useAuthStore } from '../store/useAuthStore';

export default {
  data() {
    return {
      email: "", 
      password: "", 
      rememberMe: false, 
      showPassword: false, 
      showEmailArrow: true, 
      showPasswordArrow: false, 
      emailError: false,
      passwordError: false,
      userNotFoundError: false,
      loginError: "",
      successMessage: "",
      loading: false
    };
  },
  methods: {
    validateEmail() {
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      this.emailError = !emailPattern.test(this.email);
      this.showEmailArrow = !this.emailError && this.email.trim() !== "";
    },
    async checkUserExists() {
      this.loading = true;
      try {
        const response = await axiosInstance.post('/account/check-user/', { email: this.email }); // Updated URL }); // Updated URL
        if (response.data.exists) {
          this.showPassword = true;
          this.userNotFoundError = false;
          this.showEmailArrow = false;
          this.showPasswordArrow = true;
        } else {
          this.userNotFoundError = true;
          this.showPassword = false;
        }
      } catch (error) {
        console.error("User check error:", error);
        this.userNotFoundError = true;
      } finally {
        this.loading = false;
      }
    },
    validatePassword() {
      this.passwordError = !this.password.trim();
    },
    async loginUser() {
      this.loginError = "";
      this.successMessage = "";

      // Validate email and password before making the request
      this.validateEmail();
      this.validatePassword();

      if (this.emailError || this.passwordError) return;

      this.loading = true;
      try {
        const authStore = useAuthStore();
        const redirectUrl = await authStore.login(this.email, this.password);
        this.successMessage = "Login successful! Redirecting...";
        setTimeout(() => window.location.href = redirectUrl, 2000);
      } catch (error) {
        console.error("Login error:", error); // Add console log for debugging
        if (error.response && error.response.data.errors) {
          this.loginError = error.response.data.errors.login || "Invalid email or password.";
        } else {
          this.loginError = "Login failed. Please try again.";
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
/* Body styling */
body {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 100vh;
  align-items: center;
}

/* Container styling */
.container {
  text-align: center;
  background: white;
  padding: 40px;
  border-radius: 10px;
  width: 500px;
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

/* Error message styling */
.error-message {
  color: red;
  font-size: 14px;
  margin-top: 5px;
  text-align: left;
}

/* Remember me checkbox styling */
.remember-me {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 15px;
}

/* Links styling */
.links {
  margin-top: 15px;
  font-size: 14px;
}

/* Links and router-link styling */
.links a, .links router-link {
  color: #007aff;
  text-decoration: none;
}

/* Input and arrow container */
.input-container {
  position: relative;
  width: 100%;
}

/* Arrow icon styling */
.arrow-icon {
  position: absolute;
  right: 15px;
  top: 45%;
  transform: translateY(-50%);
  cursor: pointer;
  font-size: 20px;
  color: #007aff;
}
</style>