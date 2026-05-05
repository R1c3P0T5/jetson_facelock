<script setup lang="ts">
defineOptions({
  name: 'UiSwitch',
})

const props = withDefaults(
  defineProps<{
    modelValue: boolean
    label?: string
    description?: string
    disabled?: boolean
  }>(),
  {
    label: undefined,
    description: undefined,
    disabled: false,
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const toggle = () => {
  if (props.disabled) return
  emit('update:modelValue', !props.modelValue)
}
</script>

<template>
  <div class="inline-flex items-start gap-2.5">
    <button
      type="button"
      role="switch"
      :aria-checked="modelValue"
      :aria-label="label && !description ? label : undefined"
      :disabled="disabled"
      :class="[
        'relative mt-0.5 h-5.5 w-10.5 shrink-0 rounded-full border transition-colors duration-[120ms]',
        'cursor-pointer disabled:cursor-not-allowed disabled:opacity-50',
        'focus-visible:outline focus-visible:outline-1 focus-visible:outline-ac focus-visible:outline-offset-2',
        modelValue ? 'border-ac/50 bg-ac/10' : 'border-border bg-bg',
      ]"
      @click="toggle"
      @keydown.space.prevent="toggle"
      @keydown.enter.prevent="toggle"
    >
      <span
        :class="[
          'absolute left-0.75 top-0.75 h-3.5 w-3.5 rounded-full transition-all duration-[120ms]',
          modelValue ? 'translate-x-5.5 bg-ac' : 'bg-text-placeholder',
        ]"
      />
    </button>
    <span v-if="label || description" class="grid gap-0.5">
      <span v-if="label" class="text-sm text-text-lo">{{ label }}</span>
      <span v-if="description" class="text-xs text-text-placeholder">{{ description }}</span>
    </span>
  </div>
</template>
