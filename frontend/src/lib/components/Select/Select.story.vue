<script setup lang="ts">
import { ref } from 'vue'

import Select, { type SelectOption } from './Select.vue'

defineOptions({
  name: 'UiSelectStory',
})

const mode = ref('approval')
const emptyMode = ref('')
const disabledMode = ref('always')

const modes: SelectOption[] = [
  { value: 'always', label: 'Always allow' },
  { value: 'approval', label: 'Require approval' },
  { value: 'offline', label: 'Offline only', disabled: true },
]
</script>

<template>
  <Story title="Select" :layout="{ type: 'grid', width: 320 }">
    <Variant title="Default">
      <Select v-model="mode" :options="modes" />
    </Variant>
    <Variant title="Placeholder">
      <Select v-model="emptyMode" placeholder="Choose mode" :options="modes" />
    </Variant>
    <Variant title="Invalid">
      <Select
        v-model="emptyMode"
        invalid
        error="Mode is required."
        placeholder="Choose mode"
        :options="modes"
      />
    </Variant>
    <Variant title="Disabled">
      <Select v-model="disabledMode" disabled :options="modes" />
    </Variant>
  </Story>
</template>
