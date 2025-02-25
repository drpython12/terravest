<template>
  <div class="container">
    <h2 class="title">Create Your TerraVest Account</h2>
    <p class="subtitle">One account is all you need to make sustainable investments.</p>
    <div class="links">
      <span>Already have an account? <router-link to="/account">Sign in</router-link></span>
    </div>
    <div class="input-group">
      <input v-model="firstName" type="text" class="input-box" placeholder="First name" required />
      <input v-model="surname" type="text" class="input-box" placeholder="Last name" required />
    </div>
    <input v-model="middleName" type="text" class="input-box" placeholder="Middle Name(s) (Optional)" />
    <div class="input-box select-box">
      <label class="label">Country/Region</label>
      <select v-model="country" class="select-input" required>
        <option>United Kingdom</option>
        <option>United States</option>
        <option>Canada</option>
        <option>Australia</option>
      </select>
    </div>
    <label class="label dob-label">Date of birth</label>
    <div class="dob-container">
      <select v-model="dobDay" class="dob-box" required>
        <option value="" disabled>Day</option>
        <option v-for="n in 31" :key="n" :value="n">{{ n }}</option>
      </select>
      <select v-model="dobMonth" class="dob-box" required>
        <option value="" disabled>Month</option>
        <option v-for="(month, index) in months" :key="index" :value="index+1">{{ month }}</option>
      </select>
      <select v-model="dobYear" class="dob-box" required>
        <option value="" disabled>Year</option>
        <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
      </select>
    </div>
    <p v-if="dobError" class="error-message">⚠ You must be at least 18 years old to sign up.</p>
    <input v-model="email" type="email" class="input-box" placeholder="name@example.com" required />
    <input v-model="password" type="password" class="input-box" placeholder="Password" required />
    <input v-model="confirmPassword" type="password" class="input-box" placeholder="Confirm Password" required />
    <button class="submit-btn" @click="submitForm">Continue</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      firstName: "",
      middleName: "",
      surname: "",
      country: "United Kingdom",
      dobDay: "",
      dobMonth: "",
      dobYear: "",
      email: "",
      password: "",
      confirmPassword: "",
      dobError: false,
      months: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
      years: Array.from({ length: 100 }, (_, i) => new Date().getFullYear() - i).filter(y => y <= new Date().getFullYear() - 18)
    };
  },
  methods: {
    submitForm() {
      if (!this.dobDay || !this.dobMonth || !this.dobYear) {
        this.dobError = true;
        return;
      }
      console.log("Form Submitted", this.$data);
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
  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue", Helvetica, Arial, sans-serif;
}
.container {
  text-align: center;
  background: white;
  padding: 50px;
  border-radius: 12px;
  width: 500px;
}
.title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 15px;
}
.subtitle {
  font-size: 16px;
  color: #666;
  margin-bottom: 25px;
}
.links {
  margin-bottom: 25px;
  font-size: 16px;
}
.input-group {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
}
.input-box {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 8px;
  outline: none;
  margin-bottom: 15px;
}
.dob-label {
  text-align: left;
  width: 100%;
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}
.dob-container {
  display: flex;
  gap: 10px;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 15px;
}
.dob-box {
  width: 32%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.error-message {
  color: red;
  font-size: 14px;
  margin-bottom: 15px;
}
.submit-btn {
  background: #007aff;
  color: white;
  padding: 14px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  width: 100%;
  margin-top: 15px;
}
.select-box {
  display: flex;
  flex-direction: column;
  text-align: left;
  margin-bottom: 15px;
}
.select-input {
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
}
.links a, .links router-link {
  color: #007aff;
  text-decoration: none;
}
</style>