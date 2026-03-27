import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (username, password) => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    return api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
  },
  getCurrentUser: () => api.get('/auth/me'),
};

// Ticket API
export const ticketAPI = {
  getAll: (params = {}) => api.get('/tickets/', { params }),
  getOne: (id) => api.get(`/tickets/${id}`),
  create: (data) => api.post('/tickets/', data),
  update: (id, data) => api.put(`/tickets/${id}`, data),
  delete: (id) => api.delete(`/tickets/${id}`),
  addReply: (ticketId, message, senderType = 'user') => 
    api.post(`/tickets/${ticketId}/replies`, { message, ticket_id: ticketId, sender_type: senderType }),
  getReplies: (ticketId) => api.get(`/tickets/${ticketId}/replies`),
};

// Agent API
export const agentAPI = {
  getQueue: () => api.get('/agents/queue'),
  suggestReply: (ticketId) => api.post(`/agents/suggest-reply/${ticketId}`),
  chat: (message, ticketId = null) => api.post('/agent/chat', { message, ticket_id: ticketId }),
  triage: (ticketId) => api.post(`/agent/triage/${ticketId}`),
};

// FAQ API
export const faqAPI = {
  getAll: () => api.get('/faq/'),
  getOne: (id) => api.get(`/faq/${id}`),
  create: (data) => api.post('/faq/', data),
  update: (id, data) => api.put(`/faq/${id}`, data),
  delete: (id) => api.delete(`/faq/${id}`),
};

export default api;