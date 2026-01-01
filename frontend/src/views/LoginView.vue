<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="tabs">
        <button type="button" :class="{ active: mode === 'login' }" @click="mode = 'login'">登入</button>
        <button type="button" :class="{ active: mode === 'register' }" @click="mode = 'register'">註冊</button>
      </div>

      <div v-if="mode === 'login'" class="form-section">
        <h1>歡迎回來</h1>
        <form @submit.prevent="handleLogin">
          <label>
            暱稱
            <input v-model.trim="loginForm.username" type="text" required autocomplete="username" />
          </label>
          <label>
            密碼
            <input v-model="loginForm.password" type="password" required autocomplete="current-password" />
          </label>
          <button type="submit" :disabled="loading">
            {{ loading ? '登入中...' : '登入' }}
          </button>
        </form>
      </div>

      <div v-else class="form-section">
        <h1>建立新帳號</h1>
        <form @submit.prevent="handleRegister">
          <label>
            暱稱
            <input v-model.trim="registerForm.username" type="text" required autocomplete="username" />
          </label>
          <label>
            密碼
            <input v-model="registerForm.password" type="password" required autocomplete="new-password" />
          </label>
          <button type="submit" :disabled="loading">
            {{ loading ? '送出中...' : '註冊並登入' }}
          </button>
        </form>
      </div>

      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import { sanitizeUsername } from '@/utils/sanitize'

const router = useRouter()
const route = useRoute()
const mode = ref<'login' | 'register'>('login')
const loginForm = reactive({ username: '', password: '' })
const registerForm = reactive({ username: '', password: '' })

const { loginUser, registerUser, loading, error, isAuthenticated } = useAuth()

const redirectPath = computed(() => (route.query.redirect as string) || '/')

const redirectIfAuthed = () => {
  if (isAuthenticated.value) {
    router.replace(redirectPath.value)
  }
}

watch(isAuthenticated, redirectIfAuthed, { immediate: true })

const handleLogin = async () => {
  try {
    // Sanitize username input
    const sanitizedUsername = sanitizeUsername(loginForm.username)
    await loginUser({ username: sanitizedUsername, password: loginForm.password })
    router.push(redirectPath.value)
  } catch (err) {
    // Error handled by useAuth
  }
}

const handleRegister = async () => {
  try {
    // Sanitize username input
    const sanitizedUsername = sanitizeUsername(registerForm.username)
    await registerUser({ username: sanitizedUsername, password: registerForm.password })
    router.push(redirectPath.value)
  } catch (err) {
    // Error handled by useAuth
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(180deg, #f7f9fc, #eef2f7);
  padding: 2rem 1.5rem;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  background: #ffffff;
  border-radius: 18px;
  box-shadow: 0 12px 38px rgba(15, 23, 42, 0.12);
  padding: 1.85rem;
  border: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tabs {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  overflow: hidden;
}

.tabs button {
  padding: 0.75rem 0.5rem;
  background: transparent;
  border: none;
  cursor: pointer;
  font-weight: 600;
  color: #475569;
}

.tabs button.active {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  color: #f8fafc;
}

.form-section h1 {
  margin: 0 0 0.75rem;
  font-size: 1.4rem;
  color: #111827;
}

form {
  display: grid;
  gap: 0.75rem;
}

label {
  display: grid;
  gap: 0.35rem;
  color: #1f2937;
  font-size: 0.95rem;
}

input {
  padding: 0.65rem 0.75rem;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  font-size: 1rem;
  transition: border-color 0.12s ease, box-shadow 0.12s ease;
}

input:focus-visible {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

button[type='submit'],
.tabs button {
  font-size: 1rem;
}

button[type='submit'] {
  padding: 0.65rem 0.75rem;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  color: #f8fafc;
  cursor: pointer;
  font-weight: 600;
  box-shadow: 0 12px 30px rgba(37, 99, 235, 0.35);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

button[type='submit']:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

button[type='submit']:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 16px 40px rgba(37, 99, 235, 0.45);
}

.error {
  color: #b91c1c;
  background: #fef2f2;
  border: 1px solid #fee2e2;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
}

.success {
  color: #047857;
  background: #ecfdf3;
  border: 1px solid #d1fae5;
  padding: 0.5rem 0.75rem;
  border-radius: 8px;
}
</style>
