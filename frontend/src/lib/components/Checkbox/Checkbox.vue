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
    <input
      v-bind="$attrs"
      type="checkbox"
      :checked="modelValue"
      :disabled="disabled"
      :aria-invalid="isInvalid || undefined"
      :class="[
        'mt-0.5 h-[18px] w-[18px] shrink-0 cursor-inherit accent-ac outline-offset-2 focus-visible:outline focus-visible:outline-1 focus-visible:outline-ac',
        isInvalid && 'outline outline-1 outline-err',
      ]"
      @change="update"
    />
    <span v-if="label || description" class="grid gap-0.5">
      <span v-if="label" class="text-sm text-text-hi">{{ label }}</span>
      <span v-if="description" class="text-xs text-text-placeholder">{{ description }}</span>
    </span>
  </label>
</template>
