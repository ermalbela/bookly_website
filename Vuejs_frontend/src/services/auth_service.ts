import { useAuthStore } from '@/stores/auth_store';
import api from './api';
import type { AuthResponse, AuthUser, User } from '@/types/user_types';


export const authService = {
  login: async (email: string, password: string): Promise<AuthResponse> => {
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

  get_current_user: async (): Promise<AuthUser> => {
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

  save_book: async (user_uid: string, book_uid: string): Promise<void> => {
    const {data} = await api.post(`/user_book/user/${user_uid}/book/${book_uid}`)
    return data
  },

  unsave_book: async (user_uid: string, book_uid: string): Promise<void> => {
    const {data} = await api.delete(`/user_book/user/${user_uid}/book/${book_uid}`)
    return data
  },
}