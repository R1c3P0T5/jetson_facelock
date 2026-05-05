<script setup lang="ts">
import { computed, useAttrs } from 'vue'

defineOptions({
  name: 'UiCheckbox',
  inheritAttrs: false,
})

const props = withDefaults(
  defineProps<{
    modelValue: boolean
    label?: string
    description?: string
    disabled?: boolean
    invalid?: boolean
  }>(),
  {
    label: undefined,
    description: undefined,
    disabled: false,
    invalid: false,
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const attrs = useAttrs()
const isInvalid = computed(
  () => props.invalid || attrs['aria-invalid'] === true || attrs['aria-invalid'] === 'true',
)

const update = (event: Event) => {
  if (props.disabled) return
  emit('update:modelValue', (event.target as HTMLInputElement).checked)
}
</script>

<template>
  <label
    :class="[
      'inline-flex items-start gap-2',
      disabled ? 'cursor-not-allowed opacity-60' : 'cursor-pointer',
    ]"
  >
    <span class="relative mt-0.5 inline-flex h-4.5 w-4.5 shrink-0 items-center justify-center">
      <input
        v-bind="$attrs"
        type="checkbox"
        :checked="modelValue"
        :disabled="disabled"
        :aria-invalid="isInvalid || undefined"
        :class="[
          'peer absolute inset-0 cursor-[inherit] appearance-none border bg-bg transition-colors duration-[120ms]',
          'focus-visible:outline focus-visible:outline-1 focus-visible:outline-ac focus-visible:outline-offset-2',
          'disabled:cursor-not-allowed',
          isInvalid ? 'border-err checked:border-err' : 'border-border checked:border-ac',
        ]"
        @change="update"
      />
      <span
        :class="[
          'pointer-events-none relative z-10 h-2.5 w-2.5 opacity-0 transition-opacity duration-[120ms] peer-checked:opacity-100',
          isInvalid ? 'bg-err' : 'bg-ac',
        ]"
      />
    </span>
    <span v-if="label || description" class="grid gap-0.5">
      <span v-if="label" class="text-sm text-text-hi">{{ label }}</span>
      <span v-if="description" class="text-xs text-text-placeholder">{{ description }}</span>
    </span>
  </label>
</template>
