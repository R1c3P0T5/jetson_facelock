<script setup lang="ts">
defineOptions({ name: 'UiState' })

export type StateVariant = 'empty' | 'error'

withDefaults(
  defineProps<{
    title: string
    variant?: StateVariant
    center?: boolean
  }>(),
  {
    variant: 'empty',
    center: false,
  },
)
</script>

<template>
  <div
    :class="[
      'grid gap-2 rounded-[2px] border p-4',
      center ? 'items-center justify-items-center text-center' : 'justify-items-start',
      variant === 'error'
        ? 'border-err/50 bg-err/10 text-err'
        : 'border-dashed border-border bg-element text-text-lo',
    ]"
  >
    <strong class="font-mono text-[11px] uppercase tracking-[0.08em]">{{ title }}</strong>
    <slot />
  </div>
</template>
