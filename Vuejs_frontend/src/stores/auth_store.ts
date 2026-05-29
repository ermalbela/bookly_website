import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService } from '@/services/auth_service'
import type { AuthResponse, AuthUser } from '@/types/user_types'


export const useAuthStore = defineStore('auth', () => {
  const user = ref<AuthUser | null>(null)
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'))
  const isReady = ref(false);
  
  const isAuthenticated = computed(() => !!token.value)

  const login = async (email: string, password: string) => {
    const data: AuthResponse = await authService.login(email, password)
    user.value = data.user;
    token.value = data.access_token;
    refreshToken.value = data.refresh_token;

    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)
  }

  const logout = async () => {
    await authService.logout();

    user.value = null;
    token.value = null;
    refreshToken.value = null;

    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  const fetchCurrentUser = async () => {
    if (!token.value) return
    user.value = await authService.get_current_user()
  }


  const initAuth = async () => {
  const savedToken = localStorage.getItem('access_token')
  const savedRefresh = localStorage.getItem('refresh_token')

  if (savedToken) {
    token.value = savedToken
    refreshToken.value = savedRefresh

    try {
      user.value = await authService.get_current_user()
    } catch (e) {
      await logout()
    }
  }

  isReady.value = true
}

  return { user, token, isAuthenticated, isReady, login, logout, fetchCurrentUser, initAuth }
})