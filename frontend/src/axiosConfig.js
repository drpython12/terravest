import axios from 'axios';
import Cookies from 'js-cookie';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000', // Update this to match your backend URL
  withCredentials: true, // Include credentials for cross-origin requests
});

axiosInstance.interceptors.request.use(config => {
  const csrfToken = Cookies.get('csrftoken');
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
});

export default axiosInstance;