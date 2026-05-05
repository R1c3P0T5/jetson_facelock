<script setup lang="ts">
import { computed, useAttrs } from 'vue'

defineOptions({
  name: 'UiTextarea',
  inheritAttrs: false,
})

const props = defineProps<{
  modelValue: string
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
    <textarea
      v-bind="$attrs"
      :value="modelValue"
      :aria-invalid="isInvalid || undefined"
      :class="[
        'min-h-[90px] w-full resize-y rounded-[2px] border bg-bg px-2.5 py-2 font-sans text-sm text-text-hi outline-none transition-colors duration-[120ms] placeholder:text-text-placeholder',
        'disabled:cursor-not-allowed disabled:opacity-50',
        'focus:border-ac',
        isInvalid ? 'border-err' : 'border-border',
      ]"
      @input="$emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
    />
    <p v-if="error && invalid" class="font-mono text-[11px] text-err">{{ error }}</p>
    <p v-else-if="hint" class="font-mono text-[11px] text-text-placeholder">{{ hint }}</p>
  </div>
</template>
