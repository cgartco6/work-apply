import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

// Create axios instance with base configuration
const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000, // 30 seconds
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
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

// Response interceptor to handle common errors
api.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.response?.status === 401) {
            // Token expired or invalid
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// Auth API
export const authAPI = {
    login: (credentials) => api.post('/api/auth/login', credentials),
    register: (userData) => api.post('/api/auth/register', userData),
    getProfile: () => api.get('/api/auth/profile'),
    updateProfile: (userData) => api.put('/api/auth/profile', userData),
    changePassword: (passwordData) => api.post('/api/auth/change-password', passwordData),
};

// Payments API
export const paymentsAPI = {
    initiate: (paymentData) => api.post('/api/payments/initiate', paymentData),
    getStatus: (paymentId) => api.get(`/api/payments/status/${paymentId}`),
};

// Applications API
export const applicationsAPI = {
    create: (applicationData) => api.post('/api/applications/create', applicationData),
    process: (applicationId) => api.post(`/api/applications/process/${applicationId}`),
    getHistory: () => api.get('/api/applications/history'),
    getRegions: () => api.get('/api/applications/regions'),
};

// AI Processing API
export const aiAPI = {
    enhanceResume: (data) => api.post('/api/ai/enhance-resume', data),
    generateCoverLetter: (data) => api.post('/api/ai/generate-cover-letter', data),
    optimizeATS: (data) => api.post('/api/ai/optimize-ats', data),
    processDocument: (formData) => api.post('/api/ai/process-document', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
    }),
    analyzeJobDescription: (data) => api.post('/api/ai/analyze-job-description', data),
};

export default api;
