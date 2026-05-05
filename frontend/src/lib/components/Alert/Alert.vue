<script setup lang="ts">
import { computed, ref, useSlots } from 'vue'

import Button from '../Button/Button.vue'

export type AlertVariant = 'ok' | 'info' | 'warn' | 'err' | 'dim'

defineOptions({
  name: 'UiAlert',
})

const props = withDefaults(
  defineProps<{
    variant: AlertVariant
    title?: string
    closable?: boolean
  }>(),
  {
    title: undefined,
    closable: false,
  },
)

const emit = defineEmits<{
  close: []
}>()

const open = ref(true)
const slots = useSlots()

const close = () => {
  open.value = false
  emit('close')
}

const hasHeader = computed(() => Boolean(props.title || slots.icon))

const variantClasses: Record<AlertVariant, string> = {
  ok: 'border-ok/50 bg-ok/10 text-ok',
  info: 'border-info/50 bg-info/10 text-info',
  warn: 'border-warn/50 bg-warn/10 text-warn',
  err: 'border-err/50 bg-err/10 text-err',
  dim: 'border-border bg-element text-text-lo',
}

const classes = computed(() => [
  'relative grid gap-1 rounded-[2px] border p-2.5',
  variantClasses[props.variant],
])

const bodyClasses = computed(() => [
  'text-sm opacity-90',
  !hasHeader.value && 'pt-0.5',
  props.closable && 'pr-8',
])

const closeButtonColor = {
  text: 'currentColor',
  bg: 'transparent',
  border: 'transparent',
  hoverBg: 'color-mix(in srgb, currentColor 10%, transparent)',
  hoverBorder: 'color-mix(in srgb, currentColor 35%, transparent)',
}
</script>

<template>
  <div v-if="open" :class="classes" role="alert">
    <div v-if="hasHeader" class="flex min-w-0 items-center gap-1.5 pr-8" data-test="alert-header">
      <slot name="icon" />
      <strong v-if="title" class="font-mono text-xs uppercase tracking-[0.08em]">
        {{ title }}
      </strong>
    </div>
    <Button
      v-if="closable"
      class="absolute right-1 top-1"
      variant="ghost"
      size="xs"
      :color="closeButtonColor"
      aria-label="Close alert"
      @click="close"
    >
      x
    </Button>
    <p v-if="$slots.default" :class="bodyClasses" data-test="alert-body">
      <slot />
    </p>
  </div>
</template>
