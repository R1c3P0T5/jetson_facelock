<script setup lang="ts">
import { computed, useAttrs } from 'vue'

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

const isInvalid = computed(
  () => props.invalid || attrs['aria-invalid'] === true || attrs['aria-invalid'] === 'true',
)
</script>

<template>
  <div class="grid gap-1">
    <div class="relative">
      <span
        v-if="prefix"
        data-prefix
        class="pointer-events-none absolute left-2.5 top-1/2 -translate-y-1/2 font-mono text-[11px] text-text-placeholder"
      >
        {{ prefix }}
      </span>
      <input
        v-bind="$attrs"
        :value="modelValue"
        :aria-invalid="isInvalid || undefined"
        :class="[
          'min-h-[38px] w-full rounded-[2px] border bg-bg px-2.5 py-2 font-sans text-sm text-text-hi outline-none transition-colors duration-[120ms] placeholder:text-text-placeholder',
          'disabled:cursor-not-allowed disabled:opacity-50',
          'file:border-0 file:bg-transparent file:font-mono file:text-xs file:text-text-hi',
          'focus:border-ac',
          prefix && 'pl-7',
          suffix && 'pr-10',
          isInvalid ? 'border-err' : 'border-border',
        ]"
        @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      />
      <span
        v-if="suffix"
        data-suffix
        class="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 font-mono text-[11px] text-text-placeholder"
      >
        {{ suffix }}
      </span>
    </div>
    <p v-if="error && invalid" class="font-mono text-[11px] text-err">{{ error }}</p>
    <p v-else-if="hint" class="font-mono text-[11px] text-text-placeholder">{{ hint }}</p>
  </div>
</template>
