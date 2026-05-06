<script setup lang="ts">
import { computed } from 'vue'

defineOptions({ name: 'UiProgress' })

const props = withDefaults(
  defineProps<{
    value: number
    max?: number
    label?: string
  }>(),
  {
    max: 100,
    label: undefined,
  },
)

const pct = computed(() => `${Math.min(100, Math.max(0, (props.value / props.max) * 100))}%`)
</script>

<template>
  <div
    role="progressbar"
    :aria-valuenow="value"
    :aria-valuemin="0"
    :aria-valuemax="max"
    :aria-label="label"
    class="h-2.5 overflow-hidden rounded-full border border-border bg-bg"
  >
    <div
      data-progress-bar
      class="h-full rounded-full bg-ac transition-[width] duration-300"
      :style="{ width: pct }"
    />
  </div>
</template>
