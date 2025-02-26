<template>
  <div class="container">
    <h2 class="title">Create Your TerraVest Account</h2>
    <p class="subtitle">One account is all you need to make sustainable investments.</p>
    <div class="links">
      <span>Already have an account? <router-link to="/account">Sign in</router-link></span>
    </div>
    <div class="input-group">
      <input v-model="firstName" type="text" class="input-box" placeholder="First name" @blur="validateFirstName" required />
      <input v-model="surname" type="text" class="input-box" placeholder="Last name" @blur="validateLastName" required />
    </div>
    <p v-if="nameError" class="error-message">⚠ First and last name are required.</p>
    <input v-model="middleName" type="text" class="input-box" placeholder="Middle Name(s) (Optional)" />
    <div class="input-box select-box">
      <label class="label" for="country">Country/Region</label>
      <select id="country" v-model="country" class="select-input" required>
        <option>United Kingdom</option>
        <option>United States</option>
        <option>Canada</option>
        <option>Australia</option>
      </select>
    </div>
    <label class="label dob-label" for="dobDay">Date of birth</label>
    <div class="dob-container">
      <select v-model="dobDay" class="dob-box" @blur="validateDOB" required>
        <option value="" disabled>Day</option>
        <option v-for="n in 31" :key="n" :value="n">{{ n }}</option>
      </select>
      <select v-model="dobMonth" class="dob-box" @blur="validateDOB" required>
        <option value="" disabled>Month</option>
        <option v-for="(month, index) in months" :key="index" :value="index+1">{{ month }}</option>
      </select>
      <select v-model="dobYear" class="dob-box" @blur="validateDOB" required>
        <option value="" disabled>Year</option>
        <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
      </select>
    </div>
    <p v-if="dobError" class="error-message">⚠ You must be at least 18 years old to sign up.</p>
    <input v-model="email" type="email" class="input-box" placeholder="name@example.com" @blur="validateEmail" required />
    <p v-if="emailError" class="error-message">⚠ Invalid email format.</p>
    <input v-model="password" type="password" class="input-box" placeholder="Password" @blur="validatePassword" required />
    <p v-if="passwordError" class="error-message">⚠ Password must contain at least 8 characters, a number, and a special character.</p>
    <input v-model="confirmPassword" type="password" class="input-box" placeholder="Confirm Password" @blur="validateConfirmPassword" required />
    <p v-if="confirmPasswordError" class="error-message">⚠ Passwords do not match.</p>
    <button class="submit-btn" @click="submitForm">Continue</button>
    <p v-if="successMessage" class="success-message">🎉 {{ successMessage }}</p>
    <p v-if="backendError" class="error-message">⚠ {{ backendError }}</p>
  </div>
</template>

<script>
import axios from "axios";
import Cookies from "js-cookie"; // You need to install js-cookie package

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
      nameError: false,
      dobError: false,
      emailError: false,
      passwordError: false,
      confirmPasswordError: false,
      backendError: "",
      successMessage: "",
      months: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
      years: Array.from({ length: 100 }, (_, i) => new Date().getFullYear() - i).filter(y => y <= new Date().getFullYear() - 18)
    };
  },
  methods: {
    validateFirstName() {
      this.nameError = !this.firstName.trim();
    },
    validateLastName() {
      this.nameError = !this.surname.trim();
    },
    validateDOB() {
      if (!this.dobDay || !this.dobMonth || !this.dobYear) {
        this.dobError = true;
        return;
      }
      const today = new Date();
      const birthDate = new Date(this.dobYear, this.dobMonth - 1, this.dobDay);
      const age = today.getFullYear() - birthDate.getFullYear();
      const monthDiff = today.getMonth() - birthDate.getMonth();
      if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        this.dobError = age - 1 < 18;
      } else {
        this.dobError = age < 18;
      }
    },
    validateEmail() {
      this.emailError = !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.email);
    },
    validatePassword() {
      this.passwordError = !/^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(this.password);
    },
    validateConfirmPassword() {
      this.confirmPasswordError = this.password !== this.confirmPassword;
    },
    submitForm() {
      this.backendError = "";

      // Call all validation methods
      this.validateFirstName();
      this.validateLastName();
      this.validateDOB();
      this.validateEmail();
      this.validatePassword();
      this.validateConfirmPassword();

      // Check for any validation errors
      if (this.nameError || this.dobError || this.emailError || this.passwordError || this.confirmPasswordError) return;

      // Prepare data to be sent to the backend
      const signupData = {
        first_name: this.firstName,
        middle_name: this.middleName,
        last_name: this.surname,
        country: this.country,
        date_of_birth: `${this.dobYear}-${this.dobMonth}-${this.dobDay}`,
        email: this.email,
        password: this.password,
        confirm_password: this.confirmPassword
      };

      console.log("Sending data to backend:", signupData);

      axios.post(`http://localhost:8000/signup/`, signupData, {
        headers: {
          'X-CSRFToken': Cookies.get('csrftoken'), // Include the CSRF token in the headers
          'Content-Type': 'application/json' // Ensure the content type is JSON
        }
      })
      .then(response => {
        if (response.data.success) {
          this.successMessage = response.data.message;
          setTimeout(() => window.location.href = "/account", 2000);
        }
      })
      .catch(error => {
        if (error.response && error.response.data.errors) {
          this.backendError = Object.values(error.response.data.errors).join(" ");
        }
      });
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
.success-message {
  color: green;
  font-size: 16px;
  margin-top: 10px;
  text-align: center;
}
</style>