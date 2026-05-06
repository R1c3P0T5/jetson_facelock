<script setup lang="ts">
import { ref } from 'vue'

import Badge from '../Badge/Badge.vue'
import Nav from './Nav.vue'
import NavItem from './NavItem.vue'

defineOptions({ name: 'NavStory' })

const items = [
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
  <Story title="Navigation / Nav" :layout="{ type: 'grid', width: 280 }">
    <Variant title="Items prop (controlled)">
      <Nav v-model="active" :items="items" />
    </Variant>

    <Variant title="Slot-based with badge">
      <Nav>
        <NavItem label="Overview" href="#overview" :active="true" />
        <NavItem label="Primitives" href="#primitives" />
        <NavItem label="Form controls" href="#forms" />
        <NavItem label="Feedback" href="#feedback" />
      </Nav>
    </Variant>

    <Variant title="In sidebar context">
      <div class="w-[240px] rounded-[2px] border border-border bg-subtle p-3">
        <div class="mb-3 flex items-center justify-between border-b border-border-soft pb-3">
          <span class="font-mono text-xs uppercase tracking-[0.08em] text-text-hi"
            >FaceGuard UI</span
          >
          <Badge variant="ok">v2</Badge>
        </div>
        <Nav v-model="active" :items="items" />
      </div>
    </Variant>
  </Story>
</template>
