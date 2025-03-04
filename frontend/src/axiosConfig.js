import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000', // Update this to match your backend URL
  withCredentials: true, // Include credentials for cross-origin requests
});

export default axiosInstance;