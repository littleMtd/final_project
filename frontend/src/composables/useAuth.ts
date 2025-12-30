import { computed, ref } from 'vue'
import { login, register, logout as logoutApi, getMe } from '@/api/auth'
import type { AuthUser, LoginPayload, RegisterPayload } from '@/types/auth'
import { ApiError, NetworkError, ValidationError, AuthenticationError } from '@/api/http'

const user = ref<AuthUser | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
const initialized = ref(false)

export function useAuth() {
  const isAuthenticated = computed(() => user.value !== null)

  const initAuth = async () => {
    if (initialized.value) return
    
    loading.value = true
    try {
      const response = await getMe()
      user.value = response.data?.user || null
    } catch (err) {
      // Not authenticated or session expired
      user.value = null
    } finally {
      loading.value = false
      initialized.value = true
    }
  }

  const loginUser = async (payload: LoginPayload) => {
    loading.value = true
    error.value = null
    try {
      const response = await login(payload)
      user.value = response.data?.user || null
    } catch (err) {
      if (err instanceof NetworkError) {
        error.value = '網絡連接失敗，請檢查您的網絡'
      } else if (err instanceof AuthenticationError) {
        error.value = '帳號或密碼錯誤'
      } else if (err instanceof ValidationError) {
        error.value = '輸入格式不正確'
      } else if (err instanceof ApiError) {
        error.value = err.message || '登入失敗，請稍後再試'
      } else {
        error.value = err instanceof Error ? err.message : '登入失敗'
      }
      throw err
    } finally {
      loading.value = false
    }
  }

  const registerUser = async (payload: RegisterPayload) => {
    loading.value = true
    error.value = null
    try {
      const response = await register(payload)
      // Registration returns user directly, set it
      user.value = response.data?.user || null
    } catch (err) {
      if (err instanceof NetworkError) {
        error.value = '網絡連接失敗，請檢查您的網絡'
      } else if (err instanceof ValidationError) {
        error.value = err.details?.username ? '用戶名已存在或不符合要求' : '註冊信息格式不正確'
      } else if (err instanceof ApiError) {
        error.value = err.message || '註冊失敗，請稍後再試'
      } else {
        error.value = err instanceof Error ? err.message : '註冊失敗'
      }
      throw err
    } finally {
      loading.value = false
    }
  }

  const logoutUser = async () => {
    loading.value = true
    try {
      await logoutApi()
      user.value = null
    } catch (err) {
      console.error('Logout error:', err)
      // Clear user anyway
      user.value = null
    } finally {
      loading.value = false
    }
  }

  return {
    user,
    isAuthenticated,
    loading,
    error,
    initialized,
    initAuth,
    loginUser,
    registerUser,
    logout: logoutUser
  }
}
