import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth
export const login = async (email: string, password: string) => {
  const response = await api.post('/users/login', { email, password })
  const { access_token } = response.data
  localStorage.setItem('token', access_token)
  return response.data
}

export const register = async (userData: any) => {
  const response = await api.post('/users/register', userData)
  return response.data
}

export const getCurrentUser = async () => {
  const response = await api.get('/users/me')
  return response.data
}

export const updateUser = async (userData: any) => {
  const response = await api.put('/users/me', userData)
  return response.data
}

// Analysis
export const analyzeImage = async (file: File, userNotes?: string) => {
  const formData = new FormData()
  formData.append('file', file)
  if (userNotes) {
    formData.append('user_notes', userNotes)
  }

  const response = await api.post('/analysis/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export const getAnalysisResult = async (analysisId: number) => {
  const response = await api.get(`/analysis/result/${analysisId}`)
  return response.data
}

export const deleteAnalysis = async (analysisId: number) => {
  const response = await api.delete(`/analysis/result/${analysisId}`)
  return response.data
}

// History
export const getHistory = async (limit = 10, offset = 0) => {
  const response = await api.get('/history/', {
    params: { limit, offset },
  })
  return response.data
}

export const getStats = async () => {
  const response = await api.get('/history/stats')
  return response.data
}

export const getTimeline = async (days = 30) => {
  const response = await api.get('/history/timeline', {
    params: { days },
  })
  return response.data
}

export const compareAnalyses = async (analysisId1: number, analysisId2: number) => {
  const response = await api.post(`/history/compare/${analysisId1}/${analysisId2}`)
  return response.data
}

// Recommendations
export const getConditions = async () => {
  const response = await api.get('/recommendations/conditions')
  return response.data
}

export const getConditionInfo = async (conditionName: string) => {
  const response = await api.get(`/recommendations/conditions/${conditionName}`)
  return response.data
}

export default api