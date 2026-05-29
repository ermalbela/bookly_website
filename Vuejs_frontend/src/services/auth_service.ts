import { useAuthStore } from '@/stores/auth_store';
import api from './api';
import type { AuthResponse, AuthUser, User } from '@/types/user_types';


export const authService = {
  login: async (email: string, password: string) => {
    const { data } = await api.post<AuthResponse>('/auth/login', { email, password })
    console.log(data);
    return data
  },

  register: async (username: string, email: string, password: string, first_name: string, last_name: string) => {
    const { data } = await api.post('/auth/signup', { username, email, password, first_name, last_name })
    console.log(data);
    return data
  },

  logout: async () => {
    await api.get('/auth/logout');
  },

  get_current_user: async () => {
    const { data } = await api.get<AuthUser>('/auth/me')
    return data
  },

  update_avatar: async (file: FormData) => {
    const {data} = await api.post('/auth/upload/avatar', file, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return data
  },

  requestPasswordReset: async (email: string) => {
    const { data } = await api.post('/auth/password-reset-request', { email })
    console.log(data)
    return data
  },

  confirmPasswordReset: async (token: string, new_password: string, confirm_new_password: string) => {
    const { data } = await api.post(`/auth/password-reset-confirm/${token}`, {
      new_password,
      confirm_new_password,
    })
    return data
  },
}