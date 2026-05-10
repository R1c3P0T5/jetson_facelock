<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Sidebar, Nav, Button } from '@/lib'
import type { NavItemDef } from '@/lib'
import { useAuthStore } from '@/stores/auth'

defineOptions({ name: 'AppLayout' })

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const navItems = [
  { key: 'dashboard', label: 'Dashboard', href: '/' },
  { key: 'faces', label: 'Face Management', href: '/faces' },
  { key: 'access-logs', label: 'Access Logs', href: '/access-logs' },
  { key: 'settings', label: 'Settings', href: '/settings' },
]

const activeKey = computed(() => String(route.name ?? ''))

function navigate(item: NavItemDef) {
  if (item.href) router.push(item.href)
}

function logout() {
  auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="flex min-h-screen bg-bg">
    <Sidebar brand="FaceGuard">
      <Nav :items="navItems" :model-value="activeKey" @click="navigate" />
      <template #footer>
        <div class="flex items-center justify-between gap-2">
          <span class="truncate font-mono text-[11px] text-text-lo">{{ auth.user?.username }}</span>
          <Button variant="ghost" size="xs" @click="logout">Logout</Button>
        </div>
      </template>
    </Sidebar>
    <main class="min-w-0 flex-1 p-6">
      <RouterView />
    </main>
  </div>
</template>
