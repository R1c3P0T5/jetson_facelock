<script setup lang="ts">
defineOptions({
  name: 'UiSwitch',
})

const props = withDefaults(
  defineProps<{
    modelValue: boolean
    label?: string
    disabled?: boolean
  }>(),
  {
    label: undefined,
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
  <div class="inline-flex items-center gap-2">
    <button
      type="button"
      role="switch"
      :aria-checked="modelValue"
      :aria-label="label"
      :disabled="disabled"
      :class="[
        'relative h-[22px] w-[42px] rounded-full border transition-colors duration-[120ms] cursor-pointer disabled:cursor-not-allowed disabled:opacity-50 focus-visible:outline focus-visible:outline-1 focus-visible:outline-ac focus-visible:outline-offset-2',
        modelValue ? 'border-ok/50 bg-ok/10' : 'border-border bg-bg',
      ]"
      @click="toggle"
    >
      <span
        :class="[
          'absolute top-[3px] h-[14px] w-[14px] rounded-full transition-all duration-[120ms]',
          modelValue ? 'left-[23px] bg-ok' : 'left-[3px] bg-text-placeholder',
        ]"
      />
    </button>
    <span v-if="label" class="text-sm text-text-lo">{{ label }}</span>
  </div>
</template>
