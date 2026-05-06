<script setup lang="ts">
import { ref } from 'vue'

import Badge from '../Badge/Badge.vue'
import Nav from '../Nav/Nav.vue'
import Sidebar from './Sidebar.vue'

defineOptions({ name: 'SidebarStory' })

const navItems = [
  { key: 'overview', label: 'Overview', href: '#overview' },
  { key: 'primitives', label: 'Primitives', href: '#primitives' },
  { key: 'forms', label: 'Form controls', href: '#forms' },
  { key: 'navigation', label: 'Navigation', href: '#navigation' },
  { key: 'data', label: 'Data display', href: '#data' },
  { key: 'feedback', label: 'Feedback', href: '#feedback' },
]

const active = ref('overview')
</script>

<template>
  <Story title="Navigation / Sidebar" :layout="{ type: 'single', iframe: false }">
    <Variant title="Full sidebar">
      <div class="flex h-[600px]">
        <Sidebar brand="FaceGuard UI">
          <template #brand-action>
            <Badge variant="ok">v2</Badge>
          </template>
          <template #header>
            <p class="font-mono text-[11px] uppercase tracking-[0.08em] text-text-placeholder">
              Tech / utility · Desktop
            </p>
            <div class="flex flex-wrap gap-1.5">
              <span
                v-for="chip in ['Buttons', 'Forms', 'Data', 'Overlay']"
                :key="chip"
                class="rounded-[2px] border border-border bg-element px-2 py-1 font-mono text-[11px] uppercase tracking-[0.07em] text-text-lo"
              >
                {{ chip }}
              </span>
            </div>
          </template>

          <Nav v-model="active" :items="navItems" />

          <template #footer>
            <p class="font-mono text-[11px] uppercase tracking-[0.08em] text-text-placeholder">
              Core tokens: bg / s1 / s2 · t1 / t2 / t3
            </p>
          </template>
        </Sidebar>

        <!-- Content placeholder -->
        <div class="flex flex-1 items-center justify-center bg-bg text-text-placeholder">
          <span class="font-mono text-xs uppercase tracking-[0.08em]">Main content area</span>
        </div>
      </div>
    </Variant>

    <Variant title="Minimal (brand + nav only)">
      <div class="flex h-[400px]">
        <Sidebar brand="FaceGuard">
          <Nav v-model="active" :items="navItems.slice(0, 3)" />
        </Sidebar>
        <div class="flex flex-1 items-center justify-center bg-bg text-text-placeholder">
          <span class="font-mono text-xs uppercase tracking-[0.08em]">Content</span>
        </div>
      </div>
    </Variant>
  </Story>
</template>
