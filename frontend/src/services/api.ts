import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Chat API
export const chatApi = {
  sendMessage: async (message: string) => {
    const response = await api.post('/chat/', { message })
    return response.data
  },
}

// Data API
export const dataApi = {
  getBrainWaves: async (startTime: string, endTime: string, granularity = '5min') => {
    const response = await api.get('/data/brain-waves', {
      params: { start_time: startTime, end_time: endTime, granularity },
    })
    return response.data
  },

  getStateDistribution: async (startTime: string, endTime: string) => {
    const response = await api.get('/data/state-distribution', {
      params: { start_time: startTime, end_time: endTime },
    })
    return response.data
  },

  getCognitiveScore: async (startTime: string, endTime: string) => {
    const response = await api.get('/data/cognitive-score', {
      params: { start_time: startTime, end_time: endTime },
    })
    return response.data
  },

  findPatterns: async (patternType: string, startTime: string, endTime: string) => {
    const response = await api.get('/data/patterns', {
      params: { pattern_type: patternType, start_time: startTime, end_time: endTime },
    })
    return response.data
  },
}

// Insights API
export const insightsApi = {
  getDailyInsights: async (date?: string) => {
    const response = await api.get('/insights/daily', {
      params: date ? { date } : {},
    })
    return response.data
  },

  generateInsight: async () => {
    const response = await api.get('/insights/generate')
    return response.data
  },
}

// User API
export const userApi = {
  getCurrentUser: async () => {
    const response = await api.get('/user/me')
    return response.data
  },

  getBaseline: async () => {
    const response = await api.get('/user/baseline')
    return response.data
  },
}

export default api
