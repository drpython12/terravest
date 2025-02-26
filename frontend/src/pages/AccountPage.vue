<template>
  <div class="container">
    <h2 class="title">Sign in to the TerraVest Portal</h2>
    <input 
      v-model="email" 
      type="text" 
      class="input-box" 
      placeholder="Email or Phone Number" 
      @blur="validateEmail"
    />
    <p v-if="emailError" class="error-message">⚠ Please enter a valid email address.</p>
    <input 
      v-if="showPassword" 
      v-model="password" 
      type="password" 
      class="input-box" 
      placeholder="Password"
    />
    <div v-if="error" class="error-message">Please fill in this field.</div>
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
export default {
  data() {
    return {
      email: "", // User's email or phone number
      password: "", // User's password
      rememberMe: false, // Remember me checkbox state
      error: false, // Error state for form validation
      showPassword: false, // State to show/hide password input
      emailError: false // Error state for email validation
    };
  },
  methods: {
    // Validate the email format
    validateEmail() {
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      this.emailError = !emailPattern.test(this.email);
      if (!this.emailError && this.email.trim() !== "") {
        this.showPassword = true; // Show password input if email is valid
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
</style>