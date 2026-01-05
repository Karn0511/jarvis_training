import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8574'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message = error.response?.data?.detail || error.message || 'Something went wrong'
    return Promise.reject(new Error(message))
  }
)

// API Methods
export const jarvisAPI = {
  // Health check
  getHealth: () => api.get('/'),
  
  // AI Operations
  ask: (question, model = 'gpt-4') => 
    api.post('/api/ask', { question, model }),
  
  askStream: (question, model = 'gpt-4') =>
    api.post('/api/ask/stream', { question, model }, { responseType: 'stream' }),
  
  // Code Analysis
  analyzeCode: (code, language = 'python', detailed = false) =>
    api.post('/api/analyze', { code, language, detailed }),
  
  // Chat
  chat: (messages, model = 'gpt-4') =>
    api.post('/api/chat', { messages, model }),
  
  // Command Execution
  executeCommand: (command, timeout = 30) =>
    api.post('/api/execute', { command, timeout }),
  
  // File Operations
  readFile: (filepath) =>
    api.post('/api/file/read', { filepath }),
  
  writeFile: (filepath, content) =>
    api.post('/api/file/write', { filepath, content }),
  
  // Project Initialization
  initProject: (template, path) =>
    api.post('/api/init', { template, path }),
  
  // History
  getHistory: (limit = 50) =>
    api.get(`/api/history?limit=${limit}`),
  
  clearHistory: () =>
    api.delete('/api/history'),
  
  // Stats
  getStats: () =>
    api.get('/api/stats'),
  
  // Models
  listModels: () =>
    api.get('/api/models'),
}

export default api
