import { computed, ref } from 'vue'
import { login, register } from '@/api/auth'
import type {
  AuthUser,
  LoginPayload,
  RegisterPayload
} from '@/types/auth'

const storedUser = localStorage.getItem('auth_user')

const user = ref<AuthUser | null>(storedUser ? safeParseUser(storedUser) : null)
const loading = ref(false)
const error = ref<string | null>(null)

function safeParseUser(payload: string): AuthUser | null {
  try {
    return JSON.parse(payload) as AuthUser
  } catch (err) {
    console.warn('Invalid stored user payload', err)
    return null
  }
}

const persistSession = (userData: AuthUser) => {
  localStorage.setItem('auth_user', JSON.stringify(userData))
}

const clearPersistedSession = () => {
  localStorage.removeItem('auth_user')
}

const setSession = (userData: AuthUser) => {
  user.value = userData
  persistSession(userData)
}

const clearSession = () => {
  user.value = null
  clearPersistedSession()
}

export function useAuth() {
  const isAuthenticated = computed(() => Boolean(user.value))

  const loginUser = async (payload: LoginPayload) => {
    loading.value = true
    error.value = null
    try {
      // Development: mock login for testing without backend
      if (payload.username === 'admin' && payload.password === 'admin') {
        const mockUser: AuthUser = {
          id: 'admin-001',
          username: 'admin',
          name: 'Administrator'
        }
        setSession(mockUser)
        return
      }

      // Backend returns 204, manually create user object after successful login
      await login(payload)
      const userData: AuthUser = {
        id: Date.now().toString(),
        username: payload.username
      }
      setSession(userData)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Login failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  const registerUser = async (payload: RegisterPayload) => {
    loading.value = true
    error.value = null
    try {
      // Backend returns 204, manually create user object after successful registration
      await register(payload)
      const userData: AuthUser = {
        id: Date.now().toString(),
        username: payload.username,
        name: payload.name
      }
      setSession(userData)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Register failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    clearSession()
  }

  return {
    user,
    isAuthenticated,
    loading,
    error,
    loginUser,
    registerUser,
    logout
  }
}
