<script setup lang="ts">
import { computed, ref, useAttrs, watch } from 'vue'

defineOptions({
  name: 'UiCombobox',
  inheritAttrs: false,
})

export type ComboboxOption = {
  value: string
  label: string
  disabled?: boolean
}

const props = withDefaults(
  defineProps<{
    modelValue: string
    options: ComboboxOption[]
    placeholder?: string
    emptyText?: string
    disabled?: boolean
    invalid?: boolean
    hint?: string
    error?: string
  }>(),
  {
    placeholder: 'Search option',
    emptyText: 'No options found',
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
const query = ref('')
const selectedOption = computed(() =>
  props.options.find((option) => option.value === props.modelValue),
)
const inputValue = computed(() => (open.value ? query.value : (selectedOption.value?.label ?? '')))
const isInvalid = computed(
  () => props.invalid || attrs['aria-invalid'] === true || attrs['aria-invalid'] === 'true',
)
const filteredOptions = computed(() => {
  const normalizedQuery = query.value.trim().toLowerCase()

  if (!normalizedQuery) return props.options

  return props.options.filter((option) => option.label.toLowerCase().includes(normalizedQuery))
})

watch(
  () => props.modelValue,
  () => {
    if (!open.value) query.value = ''
  },
)

const showOptions = () => {
  if (props.disabled) return

  query.value = ''
  open.value = true
}

const close = () => {
  open.value = false
  query.value = ''
}

const updateQuery = (event: Event) => {
  query.value = (event.target as HTMLInputElement).value
  open.value = true
}

const choose = (option: ComboboxOption) => {
  if (props.disabled || option.disabled) return

  emit('update:modelValue', option.value)
  close()
}
</script>

<template>
  <div class="relative grid gap-1">
    <input
      v-bind="$attrs"
      role="combobox"
      :value="inputValue"
      :placeholder="placeholder"
      :aria-expanded="open ? 'true' : 'false'"
      :aria-invalid="isInvalid || undefined"
      :disabled="disabled"
      :class="[
        'min-h-[38px] w-full rounded-[2px] border bg-bg px-2.5 py-2 font-sans text-sm text-text-hi outline-none transition-colors duration-[120ms] placeholder:text-text-placeholder',
        'disabled:cursor-not-allowed disabled:opacity-50',
        'focus:border-ac',
        isInvalid ? 'border-err' : 'border-border',
      ]"
      @focus="showOptions"
      @input="updateQuery"
      @keydown.escape.prevent="close"
    />
    <div
      v-if="open"
      role="listbox"
      class="absolute left-0 right-0 top-[42px] z-20 grid max-h-56 overflow-auto rounded-[2px] border border-border bg-overlay p-1 shadow-lg"
    >
      <p
        v-if="filteredOptions.length === 0"
        class="px-2 py-1.5 font-mono text-[11px] text-text-placeholder"
      >
        {{ emptyText }}
      </p>
      <button
        v-for="option in filteredOptions"
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
