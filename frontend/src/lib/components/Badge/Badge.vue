<script setup lang="ts">
import { computed } from 'vue'

export type BadgeVariant = 'ok' | 'info' | 'warn' | 'err' | 'dim'

defineOptions({
  name: 'UiBadge',
})

const props = withDefaults(
  defineProps<{
    variant?: BadgeVariant
  }>(),
  { variant: 'dim' },
)

const variantClasses: Record<BadgeVariant, string> = {
  ok: 'text-ok border-ok/50 bg-ok/10',
  info: 'text-info border-info/50 bg-info/10',
  warn: 'text-warn border-warn/50 bg-warn/10',
  err: 'text-err border-err/50 bg-err/10',
  dim: 'text-text-lo border-border bg-element',
}

const classes = computed(() => [
  'inline-flex items-center gap-1.5 border rounded-[2px] font-mono text-[11px] uppercase tracking-[0.07em] px-2 py-1',
  variantClasses[props.variant],
])
</script>

<template>
  <span :class="classes">
    <slot />
  </span>
</template>
