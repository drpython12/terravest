<template>
  <div class="container">
    <h2 class="title">Sign in to the TerraVest Portal</h2>
    <input 
      v-model="email" 
      type="text" 
      class="input-box" 
      placeholder="Email or Phone Number" 
      @blur="promptPassword"
    />
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
      email: "",
      password: "",
      rememberMe: false,
      error: false,
      showPassword: false
    };
  },
  methods: {
    promptPassword() {
      if (this.email.trim() !== "") {
        this.showPassword = true;
      }
    }
  }
};
</script>

<style scoped>
body {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 100vh;
  align-items: center;
}
.container {
  text-align: center;
  background: white;
  padding: 40px;
  border-radius: 10px;
  width: 500px;
}
.title {
  font-size: 22px;
  font-weight: bold;
  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue", Helvetica, Arial, sans-serif;
  margin-bottom: 20px;
}
.input-box {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  outline: none;
  margin-bottom: 10px;
}
.error-message {
  color: white;
  background: #333;
  display: inline-block;
  margin-top: 8px;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
}
.remember-me {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 15px;
}
.links {
  margin-top: 15px;
  font-size: 14px;
}
.links a, .links router-link {
  color: #007aff;
  text-decoration: none;
}
</style>
