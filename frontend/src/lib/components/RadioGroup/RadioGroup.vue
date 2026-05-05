<script setup lang="ts">
import { computed, useAttrs } from 'vue'

defineOptions({
  name: 'UiRadioGroup',
  inheritAttrs: false,
})

export type RadioGroupOption = {
  value: string
  label: string
  description?: string
  disabled?: boolean
}

const props = withDefaults(
  defineProps<{
    modelValue: string
    options: RadioGroupOption[]
    name?: string
    orientation?: 'vertical' | 'horizontal'
    disabled?: boolean
    invalid?: boolean
  }>(),
  {
    name: undefined,
    orientation: 'vertical',
    disabled: false,
    invalid: false,
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const attrs = useAttrs()
const isInvalid = computed(
  () => props.invalid || attrs['aria-invalid'] === true || attrs['aria-invalid'] === 'true',
)
const groupName = computed(() => props.name ?? `radio-group-${Math.random().toString(36).slice(2)}`)

const update = (option: RadioGroupOption) => {
  if (props.disabled || option.disabled) return
  emit('update:modelValue', option.value)
}
</script>

<template>
  <div
    v-bind="$attrs"
    role="radiogroup"
    :aria-invalid="isInvalid || undefined"
    :class="[
      orientation === 'horizontal' ? 'flex flex-wrap gap-4' : 'grid gap-2',
      disabled && 'opacity-60',
    ]"
  >
    <label
      v-for="option in options"
      :key="option.value"
      :class="[
        'inline-flex items-start gap-2',
        disabled || option.disabled ? 'cursor-not-allowed opacity-60' : 'cursor-pointer',
      ]"
    >
      <span
        class="relative mt-0.5 inline-flex h-[18px] w-[18px] shrink-0 items-center justify-center"
      >
        <input
          type="radio"
          :name="groupName"
          :value="option.value"
          :checked="modelValue === option.value"
          :disabled="disabled || option.disabled"
          :aria-invalid="isInvalid || undefined"
          :class="[
            'peer absolute inset-0 cursor-[inherit] appearance-none rounded-[2px] border bg-bg transition-colors duration-[120ms]',
            'focus-visible:outline focus-visible:outline-1 focus-visible:outline-ac focus-visible:outline-offset-2',
            'disabled:cursor-not-allowed',
            isInvalid ? 'border-err checked:border-err' : 'border-border checked:border-ac',
          ]"
          @change="update(option)"
        />
        <span
          :class="[
            'pointer-events-none relative z-10 h-[8px] w-[8px] rounded-[1px] opacity-0 transition-opacity duration-[120ms] peer-checked:opacity-100',
            isInvalid ? 'bg-err' : 'bg-ac',
          ]"
        />
      </span>
      <span class="grid gap-0.5">
        <span class="text-sm text-text-hi">{{ option.label }}</span>
        <span v-if="option.description" class="text-xs text-text-placeholder">
          {{ option.description }}
        </span>
      </span>
    </label>
  </div>
</template>
