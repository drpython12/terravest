<template>
  <div class="container">
    <!-- Title and subtitle for the signup page -->
    <h2 class="title">Create Your TerraVest Account</h2>
    <p class="subtitle">One account is all you need to make sustainable investments.</p>
    
    <!-- Link to sign in page if the user already has an account -->
    <div class="links">
      <span>Already have an account? <router-link to="/account">Sign in</router-link></span>
    </div>
    
    <!-- Input fields for first name and last name -->
    <div class="input-group">
      <input v-model="firstName" type="text" class="input-box" placeholder="First name" @blur="validateFirstName" aria-label="First name" required />
      <input v-model="surname" type="text" class="input-box" placeholder="Last name" @blur="validateLastName" aria-label="Last name" required />
    </div>
    <p v-if="nameError" class="error-message">⚠ First and last name are required.</p>
    
    <!-- Input field for middle name (optional) -->
    <input v-model="middleName" type="text" class="input-box" placeholder="Middle Name(s) (Optional)" aria-label="Middle Name(s) (Optional)" />
    
    <!-- Dropdown for selecting country/region -->
    <div class="input-box select-box">
      <label class="label" for="country">Country/Region</label>
      <select id="country" v-model="country" class="select-input" aria-label="Country/Region" required>
        <option>United Kingdom</option>
        <option>United States</option>
        <option>Canada</option>
        <option>Australia</option>
      </select>
    </div>
    
    <!-- Dropdowns for selecting date of birth -->
    <label class="label dob-label" for="dobDay">Date of birth</label>
    <div class="dob-container">
      <select v-model="dobDay" class="dob-box" @blur="validateDOB" aria-label="Day of birth" required>
        <option value="" disabled>Day</option>
        <option v-for="n in 31" :key="n" :value="n">{{ n }}</option>
      </select>
      <select v-model="dobMonth" class="dob-box" @blur="validateDOB" aria-label="Month of birth" required>
        <option value="" disabled>Month</option>
        <option v-for="(month, index) in months" :key="index" :value="index+1">{{ month }}</option>
      </select>
      <select v-model="dobYear" class="dob-box" @blur="validateDOB" aria-label="Year of birth" required>
        <option value="" disabled>Year</option>
        <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
      </select>
    </div>
    <p v-if="dobError" class="error-message">⚠ You must be at least 18 years old to sign up.</p>
    
    <!-- Input field for email -->
    <input v-model="email" type="email" class="input-box" placeholder="name@example.com" @blur="validateEmail" aria-label="Email" required />
    <p v-if="emailError" class="error-message">⚠ Invalid email format.</p>
    
    <!-- Input fields for password and confirm password -->
    <input v-model="password" type="password" class="input-box" placeholder="Password" @blur="validatePassword" aria-label="Password" required />
    <p v-if="passwordError" class="error-message">⚠ Password must contain at least 8 characters, a number, and a special character.</p>
    <input v-model="confirmPassword" type="password" class="input-box" placeholder="Confirm Password" @blur="validateConfirmPassword" aria-label="Confirm Password" required />
    <p v-if="confirmPasswordError" class="error-message">⚠ Passwords do not match.</p>
    
    <!-- Submit button for the form -->
    <button class="submit-btn" @click="submitForm" :disabled="loading">Continue</button>
    
    <!-- Success and error messages -->
    <p v-if="successMessage" class="success-message">🎉 {{ successMessage }}</p>
    <p v-if="backendError" class="error-message">⚠ {{ backendError }}</p>
  </div>
</template>

<script>
import axios from "axios";

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
      loading: false,
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
      const dob = `${this.dobYear}-${this.dobMonth}-${this.dobDay}`;
      const today = new Date();
      const birthDate = new Date(dob);
      let age = today.getFullYear() - birthDate.getFullYear();
      const monthDiff = today.getMonth() - birthDate.getMonth();
      if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
      }
      this.dobError = age < 18;
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
    async submitForm() {
      this.validateFirstName();
      this.validateLastName();
      this.validateDOB();
      this.validateEmail();
      this.validatePassword();
      this.validateConfirmPassword();

      if (this.nameError || this.dobError || this.emailError || this.passwordError || this.confirmPasswordError) {
        return;
      }

      this.loading = true;
      const data = {
        first_name: this.firstName,
        middle_name: this.middleName,
        last_name: this.surname,
        country: this.country,
        date_of_birth: `${this.dobYear}-${this.dobMonth}-${this.dobDay}`,
        email: this.email,
        password: this.password,
        confirm_password: this.confirmPassword,
      };

      try {
        const response = await axios.post('api/account/signup/', data);
        if (response.data.success) {
          this.successMessage = response.data.message;
          this.backendError = "";
          setTimeout(() => {
            this.$router.push('/login'); // Redirect to login page
          }, 2000);
        }
      } catch (error) {
        if (error.response && error.response.data.errors) {
          this.backendError = error.response.data.errors;
        } else {
          this.backendError = "An error occurred. Please try again.";
        }
      } finally {
        this.loading = false;
      }
    },
    async loginUser() {
      this.loginError = "";
      this.successMessage = "";

      // Validate email and password before making the request
      this.validateEmail();
      this.validatePassword();

      if (this.emailError || this.passwordError) return;

      try {
        const response = await axios.post(`api/account/login/`, { email: this.email, password: this.password }, {
          headers: {
            'X-CSRFToken': getCookie('csrftoken') // Assuming you have a function to get the CSRF token
          }
        });
        if (response.data.success) {
          this.successMessage = "Login successful! Redirecting...";
          setTimeout(() => window.location.href = "/dashboard", 2000);
        }
      } catch (error) {
        console.error("Login error:", error); // Add console log for debugging
        if (error.response && error.response.data.errors) {
          this.loginError = error.response.data.errors.login || "Invalid email or password.";
        } else {
          this.loginError = "Login failed. Please try again.";
        }
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
  font-family: -apple-system, BlinkMacSystemFont, "San Francisco", "Helvetica Neue", Helvetica, Arial, sans-serif;
}

/* Container styling */
.container {
  text-align: center;
  background: white;
  padding: 50px;
  border-radius: 12px;
  width: 500px;
}

/* Title styling */
.title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 15px;
}

/* Subtitle styling */
.subtitle {
  font-size: 16px;
  color: #666;
  margin-bottom: 25px;
}

/* Links styling */
.links {
  margin-bottom: 25px;
  font-size: 16px;
}

/* Input group styling */
.input-group {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
}

/* Input box styling */
.input-box {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 8px;
  outline: none;
  margin-bottom: 15px;
}

/* Date of birth label styling */
.dob-label {
  text-align: left;
  width: 100%;
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

/* Date of birth container styling */
.dob-container {
  display: flex;
  gap: 10px;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 15px;
}

/* Date of birth box styling */
.dob-box {
  width: 32%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

/* Error message styling */
.error-message {
  color: red;
  font-size: 14px;
  margin-bottom: 15px;
}

/* Submit button styling */
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

/* Select box styling */
.select-box {
  display: flex;
  flex-direction: column;
  text-align: left;
  margin-bottom: 15px;
}

/* Select input styling */
.select-input {
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

/* Links and router-link styling */
.links a, .links router-link {
  color: #007aff;
  text-decoration: none;
}

/* Success message styling */
.success-message {
  color: green;
  font-size: 16px;
  margin-top: 10px;
  text-align: center;
}
</style>