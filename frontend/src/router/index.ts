import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import FinanceView from '@/views/FinanceView-Refactored.vue'
import { useAuth } from '@/composables/useAuth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/',
      name: 'home',
      component: FinanceView
    }
  ]
})

router.beforeEach(async (to, from) => {
  const { isAuthenticated, initAuth, initialized } = useAuth()

  // Initialize auth state on first navigation
  if (!initialized.value) {
    await initAuth()
  }

  // Avoid redirect loop - if already going to login, allow it
  if (!isAuthenticated.value && to.name !== 'login') {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  if (isAuthenticated.value && to.name === 'login') {
    const redirect = (to.query.redirect as string) || '/'
    return { path: redirect }
  }

  return true
})

export default router
