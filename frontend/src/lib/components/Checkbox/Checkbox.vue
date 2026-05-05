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
    <span
      class="relative mt-0.5 inline-flex h-[18px] w-[18px] shrink-0 items-center justify-center"
    >
      <input
        v-bind="$attrs"
        type="checkbox"
        :checked="modelValue"
        :disabled="disabled"
        :aria-invalid="isInvalid || undefined"
        :class="[
          'peer absolute inset-0 cursor-[inherit] appearance-none rounded-[2px] border bg-bg transition-colors duration-[120ms]',
          'focus-visible:outline focus-visible:outline-1 focus-visible:outline-ac focus-visible:outline-offset-2',
          'disabled:cursor-not-allowed',
          isInvalid
            ? 'border-err checked:border-err checked:bg-err'
            : 'border-border checked:border-ac checked:bg-ac',
        ]"
        @change="update"
      />
      <svg
        class="pointer-events-none relative z-10 opacity-0 transition-opacity duration-[120ms] peer-checked:opacity-100"
        width="10"
        height="8"
        viewBox="0 0 10 8"
        fill="none"
        aria-hidden="true"
      >
        <path
          d="M1 3.5L3.5 6.5L9 1"
          stroke="var(--color-bg)"
          stroke-width="1.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </span>
    <span v-if="label || description" class="grid gap-0.5">
      <span v-if="label" class="text-sm text-text-hi">{{ label }}</span>
      <span v-if="description" class="text-xs text-text-placeholder">{{ description }}</span>
    </span>
  </label>
</template>
