<script setup lang="ts">
import { computed, useAttrs } from 'vue'

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
const isInvalid = computed(
  () => props.invalid || attrs['aria-invalid'] === true || attrs['aria-invalid'] === 'true',
)
</script>

<template>
  <div class="grid gap-1">
    <select
      v-bind="$attrs"
      :value="modelValue"
      :aria-invalid="isInvalid || undefined"
      :class="[
        'min-h-[38px] w-full rounded-[2px] border bg-bg px-2.5 py-2 font-sans text-sm text-text-hi outline-none transition-colors duration-[120ms]',
        'disabled:cursor-not-allowed disabled:opacity-50',
        'focus:border-ac',
        modelValue === '' && 'text-text-placeholder',
        isInvalid ? 'border-err' : 'border-border',
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
    <p v-if="error && invalid" class="font-mono text-[11px] text-err">{{ error }}</p>
    <p v-else-if="hint" class="font-mono text-[11px] text-text-placeholder">{{ hint }}</p>
  </div>
</template>
