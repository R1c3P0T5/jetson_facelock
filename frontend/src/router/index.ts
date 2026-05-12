import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const PUBLIC_PATH_PREFIXES = ['/login', '/register']

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      component: () => import('@/layouts/AuthLayout.vue'),
      children: [
        {
          path: '',
          name: 'login',
          component: () => import('@/views/LoginView.vue'),
        },
      ],
    },
    {
      path: '/register',
      component: () => import('@/layouts/AuthLayout.vue'),
      children: [
        {
          path: '',
          name: 'register',
          component: () => import('@/views/RegisterView.vue'),
        },
      ],
    },
    {
      path: '/',
      component: () => import('@/layouts/AppLayout.vue'),
      children: [
        { path: '', name: 'dashboard', component: () => import('@/views/DashboardView.vue') },
        { path: 'faces', name: 'faces', component: () => import('@/views/FacesView.vue') },
        {
          path: 'access-logs',
          name: 'access-logs',
          component: () => import('@/views/AccessLogsView.vue'),
        },
        { path: 'settings', name: 'settings', component: () => import('@/views/SettingsView.vue') },
      ],
    },
  ],
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  const isPublic = PUBLIC_PATH_PREFIXES.some((prefix) => to.path.startsWith(prefix))

  if (!auth.isAuthenticated && !isPublic) return { name: 'login' }
  if (auth.isAuthenticated && isPublic) return { name: 'dashboard' }
})

export default router
