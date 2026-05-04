<script setup lang="ts">
import { computed } from 'vue'

export type AlertVariant = 'ok' | 'info' | 'warn' | 'err' | 'dim'

defineOptions({
  name: 'UiAlert',
})

const props = defineProps<{
  variant: AlertVariant
  title: string
}>()

const variantClasses: Record<AlertVariant, string> = {
  ok: 'border-ok/50 bg-ok/10 text-ok',
  info: 'border-info/50 bg-info/10 text-info',
  warn: 'border-warn/50 bg-warn/10 text-warn',
  err: 'border-err/50 bg-err/10 text-err',
  dim: 'border-border bg-element text-text-lo',
}

const classes = computed(() => [
  'grid gap-1 rounded-[2px] border p-2.5',
  variantClasses[props.variant],
])
</script>

<template>
  <div :class="classes" role="alert">
    <strong class="font-mono text-xs uppercase tracking-[0.08em]">{{ title }}</strong>
    <p v-if="$slots.default" class="text-sm opacity-90">
      <slot />
    </p>
  </div>
</template>
