<script setup lang="ts">
import { computed, ref, useAttrs } from 'vue'

defineOptions({
  name: 'UiSelect',
  inheritAttrs: false,
})

export type SelectOption = {
  value: string
  label: string
  disabled?: boolean
}

const props = withDefaults(
  defineProps<{
    modelValue: string
    options: SelectOption[]
    placeholder?: string
    disabled?: boolean
    invalid?: boolean
    hint?: string
    error?: string
  }>(),
  {
    placeholder: 'Select option',
    disabled: false,
    invalid: false,
    hint: undefined,
    error: undefined,
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const attrs = useAttrs()
const open = ref(false)
const isInvalid = computed(
  () => props.invalid || attrs['aria-invalid'] === true || attrs['aria-invalid'] === 'true',
)
const selectedOption = computed(() =>
  props.options.find((option) => option.value === props.modelValue),
)

const toggle = () => {
  if (props.disabled) return

  open.value = !open.value
}

const close = () => {
  open.value = false
}

const choose = (option: SelectOption) => {
  if (props.disabled || option.disabled) return

  emit('update:modelValue', option.value)
  close()
}
</script>

<template>
  <div class="relative grid gap-1">
    <button
      v-bind="$attrs"
      type="button"
      aria-haspopup="listbox"
      :aria-expanded="open ? 'true' : 'false'"
      :aria-invalid="isInvalid || undefined"
      :disabled="disabled"
      :class="[
        'flex min-h-[38px] w-full items-center justify-between gap-2 rounded-[2px] border bg-bg px-2.5 py-2 text-left font-sans text-sm outline-none transition-colors duration-[120ms]',
        'disabled:cursor-not-allowed disabled:opacity-50',
        'focus:border-ac',
        selectedOption ? 'text-text-hi' : 'text-text-placeholder',
        isInvalid ? 'border-err' : 'border-border',
      ]"
      @click="toggle"
      @keydown.escape.prevent="close"
    >
      <span>{{ selectedOption?.label ?? placeholder }}</span>
      <span class="font-mono text-[11px] text-text-placeholder">v</span>
    </button>
    <div
      v-if="open"
      role="listbox"
      class="absolute left-0 right-0 top-[calc(100%-18px)] z-20 grid max-h-56 overflow-auto rounded-[2px] border border-border bg-overlay p-1 shadow-lg"
    >
      <button
        v-for="option in options"
        :key="option.value"
        type="button"
        role="option"
        :aria-selected="modelValue === option.value"
        :disabled="option.disabled"
        :data-value="option.value"
        :class="[
          'rounded-[2px] px-2 py-1.5 text-left text-sm text-text-hi outline-none transition-colors duration-[120ms]',
          'hover:bg-element focus:bg-element disabled:cursor-not-allowed disabled:opacity-50',
          modelValue === option.value && 'bg-element',
        ]"
        @click="choose(option)"
      >
        {{ option.label }}
      </button>
    </div>
    <p v-if="error && invalid" class="font-mono text-[11px] text-err">{{ error }}</p>
    <p v-else-if="hint" class="font-mono text-[11px] text-text-placeholder">{{ hint }}</p>
  </div>
</template>
