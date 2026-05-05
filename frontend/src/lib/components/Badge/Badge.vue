<script setup lang="ts">
import { computed } from 'vue'

export type BadgeVariant = 'ok' | 'info' | 'warn' | 'err' | 'dim'
export type BadgeColor =
  | string
  | {
      text: string
      bg?: string
      border?: string
    }

defineOptions({
  name: 'UiBadge',
})

const props = withDefaults(
  defineProps<{
    variant?: BadgeVariant
    color?: BadgeColor
  }>(),
  {
    variant: 'dim',
    color: undefined,
  },
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
  props.color
    ? 'text-[var(--badge-text)] border-[var(--badge-border)] bg-[var(--badge-bg)]'
    : variantClasses[props.variant],
])

const colorStyle = computed(() => {
  if (!props.color) return undefined

  const text = typeof props.color === 'string' ? props.color : props.color.text
  const bg =
    typeof props.color === 'string'
      ? `color-mix(in srgb, ${props.color} 10%, transparent)`
      : (props.color.bg ?? `color-mix(in srgb, ${props.color.text} 10%, transparent)`)
  const border =
    typeof props.color === 'string'
      ? `color-mix(in srgb, ${props.color} 50%, transparent)`
      : (props.color.border ?? `color-mix(in srgb, ${props.color.text} 50%, transparent)`)

  return {
    '--badge-text': text,
    '--badge-bg': bg,
    '--badge-border': border,
  }
})
</script>

<template>
  <span :class="classes" :style="colorStyle">
    <slot />
  </span>
</template>
