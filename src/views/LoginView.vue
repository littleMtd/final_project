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

const router = useRouter()
const route = useRoute()
const mode = ref<'login' | 'register'>('login')
const loginForm = reactive({ username: '', password: '' })
const registerForm = reactive({ username: '', name: '', password: '' })

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
    await loginUser({ ...loginForm })
    router.push(redirectPath.value)
  } catch (err) {
    
  }
}

const handleRegister = async () => {
  try {
    await registerUser({ ...registerForm })
    router.push(redirectPath.value)
  } catch (err) {
    
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #eef2ff, #f5f7fb);
  padding: 1.5rem;
}

.auth-card {
  width: 100%;
  max-width: 420px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  padding: 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.tabs {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
}

.tabs button {
  padding: 0.75rem 0.5rem;
  background: transparent;
  border: none;
  cursor: pointer;
  font-weight: 600;
  color: #4b5563;
}

.tabs button.active {
  background: #111827;
  color: white;
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
  color: #374151;
  font-size: 0.95rem;
}

input {
  padding: 0.65rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 10px;
  font-size: 1rem;
}

button[type='submit'],
.tabs button {
  font-size: 1rem;
}

button[type='submit'] {
  padding: 0.65rem 0.75rem;
  border: none;
  border-radius: 10px;
  background: #2563eb;
  color: white;
  cursor: pointer;
  font-weight: 600;
}

button[type='submit']:disabled {
  opacity: 0.65;
  cursor: not-allowed;
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
