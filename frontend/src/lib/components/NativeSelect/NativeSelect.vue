<script setup lang="ts">
import { useAttrs } from 'vue'

import { useInvalid } from '../../composables/useInvalid'

defineOptions({
  name: 'UiNativeSelect',
  inheritAttrs: false,
})

export type NativeSelectOption = {
  value: string
  label: string
  disabled?: boolean
}

const props = defineProps<{
  modelValue: string
  options: NativeSelectOption[]
  placeholder?: string
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
    <div class="relative">
      <select
        v-bind="$attrs"
        :value="modelValue"
        :aria-invalid="isInvalid || undefined"
        :class="[
          'min-h-9.5 w-full appearance-none rounded-[2px] border bg-bg py-2 pl-2.5 pr-8 font-sans text-sm text-text-hi outline-none transition-colors duration-[120ms]',
          'disabled:cursor-not-allowed disabled:opacity-50',
          'focus:border-ac focus:ring-1 focus:ring-ac/20',
          modelValue === '' && 'text-text-placeholder',
          isInvalid ? 'border-err focus:ring-err/20' : 'border-border',
        ]"
        @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
      >
        <option v-if="placeholder" value="" disabled>{{ placeholder }}</option>
        <option
          v-for="option in options"
          :key="option.value"
          :value="option.value"
          :disabled="option.disabled"
        >
          {{ option.label }}
        </option>
      </select>
      <span
        class="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 text-text-placeholder"
      >
        <svg class="h-3 w-3" viewBox="0 0 12 12" fill="none" aria-hidden="true">
          <path
            d="M2 4.5L6 8L10 4.5"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </span>
    </div>
    <p v-if="error && isInvalid" class="font-mono text-xs text-err">{{ error }}</p>
    <p v-else-if="hint" class="font-mono text-xs text-text-placeholder">{{ hint }}</p>
  </div>
</template>
