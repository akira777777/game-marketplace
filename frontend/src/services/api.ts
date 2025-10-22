import axios from 'axios';

// Получаем базовый URL из переменных окружения
const getApiBaseUrl = () => {
  // В development режиме используем proxy через Vite
  if (import.meta.env.DEV) {
    return '/api';
  }
  // В production используем переменную окружения или fallback
  return import.meta.env.VITE_API_BASE_URL || '/api';
};

export const apiClient = axios.create({
  baseURL: getApiBaseUrl(),
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor для добавления токена
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor для обработки ошибок
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
      globalThis.location.href = '/login';
    }
    throw error;
  }
);

export default apiClient;