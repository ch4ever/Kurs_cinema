import { defineStore } from 'pinia'
import api from '../api/api'

export type AuthUser = {
  id: number
  username: string
  role?: string
}

function readUserFromStorage(): AuthUser | null {
  const raw = localStorage.getItem('user')
  if (!raw) return null
  try {
    return JSON.parse(raw) as AuthUser
  } catch {
    return null
  }
}

function pickServerMessage(err: unknown): string {
  const e = err as { response?: { data?: unknown } }
  const data = e.response?.data
  if (typeof data === 'string') return data
  if (data && typeof data === 'object') {
    const d = data as Record<string, unknown>
    if (typeof d.detail === 'string') return d.detail
    if (Array.isArray(d.non_field_errors) && typeof d.non_field_errors[0] === 'string') {
      return d.non_field_errors[0]
    }
    const flat = Object.values(d).flat()[0]
    if (typeof flat === 'string') return flat
    if (Array.isArray(flat) && typeof flat[0] === 'string') return flat[0]
  }
  return 'Ошибка запроса'
}

function messageFromAxios(err: unknown): string {
  const e = err as { response?: { status?: number }; message?: string }
  if (e.response?.status === 401) return 'Неверный логин или пароль'
  if (e.response?.status === 400) return pickServerMessage(err)
  if (e.message) return e.message
  return 'Нет ответа от сервера'
}

export const userStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('accessToken') as string | null,
    user: readUserFromStorage(),
    authModalOpen: false,
    authModalTab: 'login' as 'login' | 'register',
  }),

  getters: {
    isAuthenticated: (state) => Boolean(state.token),
    username: (state) => state.user?.username ?? '',
    isAdmin: (state) => state.user?.role === 'Admins',
  },

  actions: {
    openAuthModal(tab: 'login' | 'register' = 'login') {
      this.authModalTab = tab
      this.authModalOpen = true
    },

    closeAuthModal() {
      this.authModalOpen = false
    },

    setToken(token: string | null) {
      this.token = token
      if (token) localStorage.setItem('accessToken', token)
      else localStorage.removeItem('accessToken')
    },

    setUser(user: AuthUser | null) {
      this.user = user
      if (user) localStorage.setItem('user', JSON.stringify(user))
      else localStorage.removeItem('user')
    },

    async login(username: string, password: string) {
      try {
        const { data } = await api.post<{ access: string; refresh: string }>('login/', {
          username,
          password,
        })
        this.setToken(data.access)
        localStorage.setItem('refreshToken', data.refresh)
        const profile = await api.get<AuthUser>('getme/')
        this.setUser(profile.data)
        this.closeAuthModal()
      } catch (err) {
        throw new Error(messageFromAxios(err))
      }
    },

    async register(username: string, password: string) {
      try {
        const { data } = await api.post<{ access: string; refresh: string }>('register/', {
          username,
          password,
        })
        this.setToken(data.access)
        localStorage.setItem('refreshToken', data.refresh)
        const profile = await api.get<AuthUser>('getme/')
        this.setUser(profile.data)
        this.closeAuthModal()
      } catch (err) {
        throw new Error(messageFromAxios(err))
      }
    },

    logout() {
      this.setToken(null)
      this.setUser(null)
      localStorage.removeItem('refreshToken')
    },

    async initFromStore() {
      if (!this.token) return
      if (this.user) return
      try {
        const profile = await api.get<AuthUser>('getme/')
        this.setUser(profile.data)
      } catch {
        this.logout()
      }
    },
  },
})
