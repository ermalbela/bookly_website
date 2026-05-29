import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth_store'
import { authService } from '@/services/auth_service'
import type { AuthResponse, AuthUser } from '@/types/user_types'

// ─── Mock authService ────────────────────────────────────────────────────────
vi.mock('@/services/auth_service', () => ({
  authService: {
    login: vi.fn(),
    logout: vi.fn(),
    get_current_user: vi.fn(),
  },
}))

// ─── Mock localStorage ───────────────────────────────────────────────────────
const localStorageMock = (() => {
  let store: Record<string, string> = {}
  return {
    getItem: (key: string) => store[key] ?? null,
    setItem: (key: string, value: string) => { store[key] = value },
    removeItem: (key: string) => { delete store[key] },
    clear: () => { store = {} },
  }
})()

Object.defineProperty(window, 'localStorage', { value: localStorageMock })

// ─── Shared mock data ────────────────────────────────────────────────────────
const mockUser: AuthUser = {
  uid: 'user-123',
  email: 'ermal@test.com',
  username: 'ermali1',
  role: 'user',
  avatar_url: 'https://res.cloudinary.com/example.jpg',
}

const mockAuthResponse: AuthResponse = {
  access_token: 'access-token-abc',
  refresh_token: 'refresh-token-xyz',
  message: 'Login successful',
  user: {
    uid: 'user-123',
    email: 'ermal@test.com',
    username: 'ermali1',
    role: 'user',
    avatar_url: 'https://res.cloudinary.com/example.jpg',
  }
}

// ─── Setup ───────────────────────────────────────────────────────────────────
beforeEach(() => {
  setActivePinia(createPinia())
  localStorageMock.clear()
  vi.clearAllMocks()
})

// ─── login ───────────────────────────────────────────────────────────────────
describe('login', () => {
  it('sets user, token, and refreshToken on successful login', async () => {
    vi.mocked(authService.login).mockResolvedValue(mockAuthResponse)
    const auth = useAuthStore()

    await auth.login('ermal@test.com', 'password123')

    expect(auth.user).toEqual(mockAuthResponse.user)
    expect(auth.token).toBe('access-token-abc')
    expect(auth.isAuthenticated).toBe(true)
  })

  it('saves tokens to localStorage on successful login', async () => {
    vi.mocked(authService.login).mockResolvedValue(mockAuthResponse)
    const auth = useAuthStore()

    await auth.login('ermal@test.com', 'password123')

    expect(localStorage.getItem('access_token')).toBe('access-token-abc')
    expect(localStorage.getItem('refresh_token')).toBe('refresh-token-xyz')
  })

  it('calls authService.login with correct credentials', async () => {
    vi.mocked(authService.login).mockResolvedValue(mockAuthResponse)
    const auth = useAuthStore()

    await auth.login('ermal@test.com', 'password123')

    expect(authService.login).toHaveBeenCalledWith('ermal@test.com', 'password123')
    expect(authService.login).toHaveBeenCalledTimes(1)
  })

  it('throws and does not set state when login fails', async () => {
    vi.mocked(authService.login).mockRejectedValue(new Error('Invalid credentials'))
    const auth = useAuthStore()

    await expect(auth.login('wrong@test.com', 'wrongpass')).rejects.toThrow('Invalid credentials')

    expect(auth.user).toBeNull()
    expect(auth.token).toBeNull()
    expect(auth.isAuthenticated).toBe(false)
  })
})

// ─── logout ──────────────────────────────────────────────────────────────────
describe('logout', () => {
  it('clears user, token, and refreshToken', async () => {
    vi.mocked(authService.login).mockResolvedValue(mockAuthResponse)
    vi.mocked(authService.logout).mockResolvedValue(undefined)
    const auth = useAuthStore()

    await auth.login('ermal@test.com', 'password123')
    await auth.logout()

    expect(auth.user).toBeNull()
    expect(auth.token).toBeNull()
    expect(auth.isAuthenticated).toBe(false)
  })

  it('removes tokens from localStorage', async () => {
    vi.mocked(authService.login).mockResolvedValue(mockAuthResponse)
    vi.mocked(authService.logout).mockResolvedValue(undefined)
    const auth = useAuthStore()

    await auth.login('ermal@test.com', 'password123')
    await auth.logout()

    expect(localStorage.getItem('access_token')).toBeNull()
    expect(localStorage.getItem('refresh_token')).toBeNull()
  })

  it('calls authService.logout', async () => {
    vi.mocked(authService.logout).mockResolvedValue(undefined)
    const auth = useAuthStore()

    await auth.logout()

    expect(authService.logout).toHaveBeenCalledTimes(1)
  })
})

// ─── initAuth ────────────────────────────────────────────────────────────────
describe('initAuth', () => {
  it('sets user from API when token exists in localStorage', async () => {
    localStorage.setItem('access_token', 'saved-token')
    localStorage.setItem('refresh_token', 'saved-refresh')
    vi.mocked(authService.get_current_user).mockResolvedValue(mockUser)
    const auth = useAuthStore()

    await auth.initAuth()

    expect(auth.user).toEqual(mockUser)
    expect(auth.token).toBe('saved-token')
    expect(auth.isReady).toBe(true)
  })

  it('sets isReady to true even when no token in localStorage', async () => {
    const auth = useAuthStore()

    await auth.initAuth()

    expect(auth.isReady).toBe(true)
    expect(auth.user).toBeNull()
    expect(authService.get_current_user).not.toHaveBeenCalled()
  })

  it('calls logout and sets isReady when get_current_user fails', async () => {
    localStorage.setItem('access_token', 'expired-token')
    vi.mocked(authService.get_current_user).mockRejectedValue(new Error('Unauthorized'))
    vi.mocked(authService.logout).mockResolvedValue(undefined)
    const auth = useAuthStore()

    await auth.initAuth()

    expect(auth.user).toBeNull()
    expect(auth.token).toBeNull()
    expect(localStorage.getItem('access_token')).toBeNull()
    expect(auth.isReady).toBe(true)
  })

  it('does not fetch user when no token is saved', async () => {
    const auth = useAuthStore()

    await auth.initAuth()

    expect(authService.get_current_user).not.toHaveBeenCalled()
  })
})

// ─── isAuthenticated ─────────────────────────────────────────────────────────
describe('isAuthenticated', () => {
  it('is false by default', () => {
    const auth = useAuthStore()
    expect(auth.isAuthenticated).toBe(false)
  })

  it('is true when token is set', async () => {
    vi.mocked(authService.login).mockResolvedValue(mockAuthResponse)
    const auth = useAuthStore()

    await auth.login('ermal@test.com', 'password123')

    expect(auth.isAuthenticated).toBe(true)
  })

  it('is false after logout', async () => {
    vi.mocked(authService.login).mockResolvedValue(mockAuthResponse)
    vi.mocked(authService.logout).mockResolvedValue(undefined)
    const auth = useAuthStore()

    await auth.login('ermal@test.com', 'password123')
    await auth.logout()

    expect(auth.isAuthenticated).toBe(false)
  })
})