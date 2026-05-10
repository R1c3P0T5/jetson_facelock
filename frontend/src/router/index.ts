import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

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
  const isPublic = to.path.startsWith('/login')

  if (!auth.isAuthenticated && !isPublic) return { name: 'login' }
  if (auth.isAuthenticated && isPublic) return { name: 'dashboard' }
})

export default router
