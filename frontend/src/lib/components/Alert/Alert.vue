<script setup lang="ts">
import { computed, ref, useSlots } from 'vue'

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

const hasHeader = computed(() => Boolean(props.title || slots.icon || props.closable))

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
  <div v-if="open" :class="classes" role="alert">
    <div v-if="hasHeader" class="flex items-start justify-between gap-2">
      <div data-test="alert-header" class="flex min-w-0 items-center gap-1.5">
        <slot name="icon" />
        <strong v-if="title" class="font-mono text-xs uppercase tracking-[0.08em]">
          {{ title }}
        </strong>
      </div>
      <button
        v-if="closable"
        type="button"
        class="-m-1 inline-flex size-6 shrink-0 items-center justify-center rounded-[2px] font-mono text-xs opacity-70 transition-opacity hover:opacity-100 focus-visible:outline focus-visible:outline-1 focus-visible:outline-current focus-visible:outline-offset-2"
        aria-label="Close alert"
        @click="close"
      >
        <span aria-hidden="true">x</span>
      </button>
    </div>
    <p v-if="$slots.default" class="text-sm opacity-90">
      <slot />
    </p>
  </div>
</template>
