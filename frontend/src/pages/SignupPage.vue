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
      <input v-model="firstName" type="text" class="input-box" placeholder="First name" @blur="validateFirstName" required />
      <input v-model="surname" type="text" class="input-box" placeholder="Last name" @blur="validateLastName" required />
    </div>
    <p v-if="nameError" class="error-message">⚠ First and last name are required.</p>
    
    <!-- Input field for middle name (optional) -->
    <input v-model="middleName" type="text" class="input-box" placeholder="Middle Name(s) (Optional)" />
    
    <!-- Dropdown for selecting country/region -->
    <div class="input-box select-box">
      <label class="label" for="country">Country/Region</label>
      <select id="country" v-model="country" class="select-input" required>
        <option>United Kingdom</option>
        <option>United States</option>
        <option>Canada</option>
        <option>Australia</option>
      </select>
    </div>
    
    <!-- Dropdowns for selecting date of birth -->
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
    
    <!-- Input field for email -->
    <input v-model="email" type="email" class="input-box" placeholder="name@example.com" @blur="validateEmail" required />
    <p v-if="emailError" class="error-message">⚠ Invalid email format.</p>
    
    <!-- Input fields for password and confirm password -->
    <input v-model="password" type="password" class="input-box" placeholder="Password" @blur="validatePassword" required />
    <p v-if="passwordError" class="error-message">⚠ Password must contain at least 8 characters, a number, and a special character.</p>
    <input v-model="confirmPassword" type="password" class="input-box" placeholder="Confirm Password" @blur="validateConfirmPassword" required />
    <p v-if="confirmPasswordError" class="error-message">⚠ Passwords do not match.</p>
    
    <!-- Submit button for the form -->
    <button class="submit-btn" @click="submitForm">Continue</button>
    
    <!-- Success and error messages -->
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
      firstName: "", // User's first name
      middleName: "", // User's middle name (optional)
      surname: "", // User's last name
      country: "United Kingdom", // User's country/region
      dobDay: "", // Day of birth
      dobMonth: "", // Month of birth
      dobYear: "", // Year of birth
      email: "", // User's email
      password: "", // User's password
      confirmPassword: "", // User's confirm password
      nameError: false, // Error state for name validation
      dobError: false, // Error state for date of birth validation
      emailError: false, // Error state for email validation
      passwordError: false, // Error state for password validation
      confirmPasswordError: false, // Error state for confirm password validation
      backendError: "", // Error message from backend
      successMessage: "", // Success message from backend
      months: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], // Months for date of birth dropdown
      years: Array.from({ length: 100 }, (_, i) => new Date().getFullYear() - i).filter(y => y <= new Date().getFullYear() - 18) // Years for date of birth dropdown
    };
  },
  methods: {
    // Validate the first name
    validateFirstName() {
      this.nameError = !this.firstName.trim();
    },
    // Validate the last name
    validateLastName() {
      this.nameError = !this.surname.trim();
    },
    // Validate the date of birth
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
    // Validate the email format
    validateEmail() {
      this.emailError = !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.email);
    },
    // Validate the password format
    validatePassword() {
      this.passwordError = !/^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/.test(this.password);
    },
    // Validate that the confirm password matches the password
    validateConfirmPassword() {
      this.confirmPasswordError = this.password !== this.confirmPassword;
    },
    // Submit the form data to the backend
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

      // Send the data to the backend using Axios
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