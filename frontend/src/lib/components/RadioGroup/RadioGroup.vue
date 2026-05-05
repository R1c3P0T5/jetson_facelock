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
      <input
        type="radio"
        :name="groupName"
        :value="option.value"
        :checked="modelValue === option.value"
        :disabled="disabled || option.disabled"
        :aria-invalid="isInvalid || undefined"
        :class="[
          'mt-0.5 h-[18px] w-[18px] shrink-0 cursor-inherit accent-ac outline-offset-2 focus-visible:outline focus-visible:outline-1 focus-visible:outline-ac',
          isInvalid && 'outline outline-1 outline-err',
        ]"
        @change="update(option)"
      />
      <span class="grid gap-0.5">
        <span class="text-sm text-text-hi">{{ option.label }}</span>
        <span v-if="option.description" class="text-xs text-text-placeholder">
          {{ option.description }}
        </span>
      </span>
    </label>
  </div>
</template>
