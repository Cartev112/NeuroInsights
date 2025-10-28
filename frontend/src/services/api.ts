import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL

if (!API_URL) {
  console.warn('[API] VITE_API_URL is undefined; requests may fail')
} else {
  console.debug('[API] Using base URL', API_URL)
}

const api = axios.create({
  baseURL: `${API_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(
  (config) => {
    console.debug('[API request]', {
      method: config.method?.toUpperCase(),
      url: config.baseURL ? `${config.baseURL}${config.url}` : config.url,
      params: config.params,
      data: config.data,
    })
    return config
  },
  (error) => {
    console.error('[API request error]', error)
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => {
    console.debug('[API response]', {
      status: response.status,
      url: response.config.url,
      data: response.data,
    })
    return response
  },
  (error) => {
    if (error.response) {
      console.error('[API response error]', {
        status: error.response.status,
        url: error.config?.url,
        data: error.response.data,
      })
    } else {
      console.error('[API response error]', error)
    }
    return Promise.reject(error)
  }
)

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
