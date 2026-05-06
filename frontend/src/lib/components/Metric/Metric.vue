<script setup lang="ts">
defineOptions({ name: 'UiMetric' })

defineProps<{
  label: string
  value: string | number
  delta?: string
}>()
</script>

<template>
  <div class="grid gap-1 rounded-[2px] border border-border bg-element p-2.5">
    <p class="font-mono text-[11px] uppercase tracking-[0.08em] text-text-placeholder">
      {{ label }}
    </p>
    <p class="font-mono text-2xl tabular-nums tracking-[0.02em] text-text-hi">
      {{ value }}
    </p>
    <p v-if="delta" data-metric-delta class="text-xs text-text-lo">{{ delta }}</p>
  </div>
</template>
