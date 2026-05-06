<script setup lang="ts">
import { ref } from 'vue'

import Tabs from './Tabs.vue'

defineOptions({ name: 'TabsStory' })

const active = ref('live')
const tabs = [
  { key: 'live', label: 'Live logs' },
  { key: 'alerts', label: 'Alerts' },
  { key: 'audit', label: 'Audit' },
]
</script>

<template>
  <Story title="Navigation / Tabs" :layout="{ type: 'single', iframe: false }">
    <Variant title="Default">
      <Tabs v-model="active" :tabs="tabs">
        <template #live><p class="text-sm text-text-lo">Live log content here.</p></template>
        <template #alerts><p class="text-sm text-text-lo">No critical alerts.</p></template>
        <template #audit><p class="text-sm text-text-lo">Audit trail content.</p></template>
      </Tabs>
    </Variant>
  </Story>
</template>
