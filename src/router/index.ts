import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import FinanceView from '@/views/FinanceView.vue'
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

router.beforeEach((to) => {
  const { isAuthenticated } = useAuth()

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
