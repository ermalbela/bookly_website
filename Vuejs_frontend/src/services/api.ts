import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

let isRefreshing = false
let failedQueue: { resolve: (token: string) => void; reject: (err: any) => void }[] = []

const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach((p) => {
    if (error) p.reject(error)
    else p.resolve(token!)
  })
  failedQueue = []
}

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const originalRequest = err.config

    // if not 401 or already retried reject immediately
    if (err.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(err)
    }

    const storedRefreshToken = localStorage.getItem('refresh_token')

    // no refresh token, log out
    if (!storedRefreshToken) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.location.href = '/auth/login'
      return Promise.reject(err)
    }

    // if already refreshing, queue this request until done
    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        failedQueue.push({ resolve, reject })
      }).then((token) => {
        originalRequest.headers.Authorization = `Bearer ${token}`
        return api(originalRequest)
      })
    }

    originalRequest._retry = true
    isRefreshing = true

    try {
      const { data } = await axios.get(import.meta.env.VITE_BASE_URL + '/auth/refresh_token', {
        headers: {
          Authorization: `Bearer ${storedRefreshToken}`
        }
      })

      const newAccessToken = data.access_token
      localStorage.setItem('access_token', newAccessToken)

      api.defaults.headers.Authorization = `Bearer ${newAccessToken}`
      originalRequest.headers.Authorization = `Bearer ${newAccessToken}`

      processQueue(null, newAccessToken)
      return api(originalRequest)

    } catch (refreshError) {
      processQueue(refreshError, null)
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.location.href = '/auth/login'
      console.log(refreshError)
      return Promise.reject(refreshError)

    } finally {
      isRefreshing = false
    }
  }
)

export default api