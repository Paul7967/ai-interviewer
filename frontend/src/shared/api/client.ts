import axios from 'axios';

// В development используем относительные пути для работы через Vite proxy
// В production используем полный URL
const API_BASE_URL = import.meta.env.DEV 
  ? '' // Пустая строка для относительных путей
  : (import.meta.env.VITE_API_URL || 'http://localhost:8000');

// Создание axios инстанса
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 секунд таймаут
});

// Интерцепторы для обработки ошибок
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    
    // Обработка различных типов ошибок
    if (error.response) {
      // Сервер ответил с ошибкой
      const { status, data } = error.response;
      
      switch (status) {
        case 400:
          console.error('Bad Request:', data);
          break;
        case 404:
          console.error('Not Found:', data);
          break;
        case 500:
          console.error('Server Error:', data);
          break;
        default:
          console.error(`HTTP Error ${status}:`, data);
      }
    } else if (error.request) {
      // Запрос был отправлен, но ответ не получен
      console.error('Network Error: No response received');
    } else {
      // Ошибка при настройке запроса
      console.error('Request Error:', error.message);
    }
    
    return Promise.reject(error);
  }
);

// Интерцептор для логирования запросов (в development)
if (import.meta.env.DEV) {
  apiClient.interceptors.request.use(
    (config) => {
      console.log(`🚀 ${config.method?.toUpperCase()} ${config.url}`, config.data);
      return config;
    },
    (error) => {
      console.error('Request Error:', error);
      return Promise.reject(error);
    }
  );
}

