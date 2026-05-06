<script setup lang="ts">
import { useAttrs } from 'vue'

import { useInvalid } from '../../composables/useInvalid'

defineOptions({
  name: 'UiInput',
  inheritAttrs: false,
})

const props = defineProps<{
  modelValue: string
  prefix?: string
  suffix?: string
  invalid?: boolean
  hint?: string
  error?: string
}>()

defineEmits<{
  'update:modelValue': [value: string]
}>()

const attrs = useAttrs()
const isInvalid = useInvalid(props, attrs)
</script>

<template>
  <div class="grid gap-1">
    <div class="relative flex items-center">
      <span
        v-if="prefix"
        data-prefix
        class="pointer-events-none absolute left-0 top-0 flex h-full items-center rounded-l-[2px] border-r border-border bg-element px-2.5 font-mono text-xs text-text-placeholder"
      >
        {{ prefix }}
      </span>
      <input
        v-bind="$attrs"
        :value="modelValue"
        :aria-invalid="isInvalid || undefined"
        :class="[
          'min-h-9.5 w-full rounded-[2px] border bg-bg py-2 font-sans text-sm text-text-hi outline-none transition-colors duration-[120ms] placeholder:text-text-placeholder',
          'disabled:cursor-not-allowed disabled:opacity-50',
          'file:border-0 file:bg-transparent file:font-mono file:text-xs file:text-text-hi',
          'focus:border-ac focus:ring-1 focus:ring-ac/20',
          prefix ? 'pl-10 pr-2.5' : 'px-2.5',
          suffix && 'pr-9',
          isInvalid ? 'border-err focus:ring-err/20' : 'border-border',
        ]"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      />
      <span
        v-if="suffix"
        data-suffix
        class="pointer-events-none absolute right-2.5 font-mono text-xs text-text-placeholder"
      >
        {{ suffix }}
      </span>
    </div>
    <p v-if="error && isInvalid" class="font-mono text-xs text-err">{{ error }}</p>
    <p v-else-if="hint" class="font-mono text-xs text-text-placeholder">{{ hint }}</p>
  </div>
</template>
