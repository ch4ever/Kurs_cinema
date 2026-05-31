import axios from 'axios'

const API_URL = '/api/'

const api = axios.create({
  baseURL: API_URL,
  timeout: 5000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken')
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refreshToken')
        if (!refreshToken) throw new Error('No refreshToken')
        const { data } = await axios.post(`${API_URL}token/refresh/`, {
          refresh: refreshToken,
        })
        localStorage.setItem('accessToken', data.access)
        const { userStore: getUserStore } = await import('../stores/user')
        getUserStore().setToken(data.access)
        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${data.access}`
        }
        return api(originalRequest)
      } catch {
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        localStorage.removeItem('user')

        const { userStore } = await import('../stores/user')
        const store = userStore()
        store.setToken(null)
        store.setUser(null)
        store.openAuthModal('login')
        const { useAlertStore } = await import('../stores/alerts')
        useAlertStore().showErrorAlert('Session expired. Please, log in')
      }
    }
    if (error.response?.status !== 401) {
      const { useAlertStore } = await import('../stores/alerts')
      const alerts = useAlertStore()

      if (!error.response) {
        alerts.showErrorAlert('Network error')
      } else {
        const data = error.response.data

        if (data.detail) {
          alerts.showErrorAlert(data.detail)
        } 
        else if (typeof data === 'object') {
          const errorMessages = Object.entries(data)
            .map(([field, messages]) => {
              const msg = Array.isArray(messages) ? messages.join(' ') : String(messages)
              return `${field}: ${msg}`
            })
            .join('<br>') 
            
          alerts.showErrorAlert(errorMessages || 'Data validation error')
        } else {
          alerts.showErrorAlert('Server error')
        }
      }
    }
    return Promise.reject(error)
  },
)

export default api
