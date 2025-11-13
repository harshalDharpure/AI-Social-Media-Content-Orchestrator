import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Content API
export const contentAPI = {
  generate: (data) => api.post('/api/content/generate', data),
  generateVariations: (data, count = 3) => api.post(`/api/content/generate/variations?count=${count}`, data),
  brainstorm: (data) => api.post('/api/content/brainstorm', data),
}

// Scheduling API
export const schedulingAPI = {
  schedule: (data) => api.post('/api/scheduling/schedule', data),
  getScheduled: () => api.get('/api/scheduling/scheduled'),
  cancel: (id) => api.delete(`/api/scheduling/scheduled/${id}`),
}

// Analytics API
export const analyticsAPI = {
  getAnalytics: (data) => api.post('/api/analytics/', data),
  getPlatformAnalytics: (platform, days = 7) => 
    api.get(`/api/analytics/platform/${platform}?days=${days}`),
}

// Social Media API
export const socialMediaAPI = {
  post: (data) => api.post('/api/social-media/post', data),
  getPlatforms: () => api.get('/api/social-media/platforms'),
}

// Images API
export const imagesAPI = {
  generate: (data) => api.post('/api/images/generate', data),
  analyze: (imageUrl) => api.post('/api/images/analyze', { image_url: imageUrl }),
}

// RAG API
export const ragAPI = {
  upload: (data) => api.post('/api/rag/upload', data),
  uploadFile: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/api/rag/upload/file', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  search: (query, topK = 5) => api.post(`/api/rag/search?query=${query}&top_k=${topK}`),
  delete: (id) => api.delete(`/api/rag/document/${id}`),
}

export default api

