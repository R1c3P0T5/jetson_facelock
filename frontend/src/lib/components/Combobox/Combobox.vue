<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, useAttrs } from 'vue'

import { useInvalid } from '../../composables/useInvalid'

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
const root = ref<HTMLElement>()
const open = ref(false)
const query = ref('')
const selectedOption = computed(() =>
  props.options.find((option) => option.value === props.modelValue),
)
const inputValue = computed(() => (open.value ? query.value : (selectedOption.value?.label ?? '')))
const isInvalid = useInvalid(props, attrs)
const filteredOptions = computed(() => {
  const normalizedQuery = query.value.trim().toLowerCase()
  if (!normalizedQuery) return props.options
  return props.options.filter((option) => option.label.toLowerCase().includes(normalizedQuery))
})

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

const clear = () => {
  emit('update:modelValue', '')
  close()
}

const onDocClick = (e: MouseEvent) => {
  if (open.value && !root.value?.contains(e.target as Node)) {
    close()
  }
}

onMounted(() => document.addEventListener('mousedown', onDocClick))
onBeforeUnmount(() => document.removeEventListener('mousedown', onDocClick))
</script>

<template>
  <div ref="root" class="grid gap-1">
    <div class="relative">
      <input
        v-bind="$attrs"
        role="combobox"
        :value="inputValue"
        :placeholder="placeholder"
        :aria-expanded="open ? 'true' : 'false'"
        :aria-invalid="isInvalid || undefined"
        :disabled="disabled"
        :class="[
          'min-h-9.5 w-full rounded-[2px] border bg-bg py-2 pl-2.5 pr-8 font-sans text-sm text-text-hi outline-none transition-colors duration-[120ms] placeholder:text-text-placeholder',
          'disabled:cursor-not-allowed disabled:opacity-50',
          'focus:border-ac focus:ring-1 focus:ring-ac/20',
          isInvalid ? 'border-err focus:ring-err/20' : 'border-border',
        ]"
        @focus="showOptions"
        @input="updateQuery"
        @keydown.escape.prevent="close"
      />
      <button
        v-if="selectedOption && !open"
        type="button"
        tabindex="-1"
        aria-hidden="true"
        class="absolute right-2.5 top-1/2 -translate-y-1/2 text-text-placeholder transition-colors duration-[120ms] hover:text-text-hi"
        @click.stop="clear"
      >
        <svg class="h-3 w-3" viewBox="0 0 12 12" fill="none">
          <path
            d="M2 2L10 10M10 2L2 10"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
          />
        </svg>
      </button>
      <span
        v-else
        class="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 text-text-placeholder"
      >
        <svg
          :class="['h-3 w-3 transition-transform duration-[120ms]', open && 'rotate-180']"
          viewBox="0 0 12 12"
          fill="none"
          aria-hidden="true"
        >
          <path
            d="M2 4.5L6 8L10 4.5"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </span>
      <div
        v-if="open"
        role="listbox"
        class="absolute left-0 right-0 top-full z-20 mt-1 grid max-h-56 overflow-auto rounded-[2px] border border-border bg-overlay p-1 shadow-lg"
      >
        <p
          v-if="filteredOptions.length === 0"
          class="px-2 py-1.5 font-mono text-xs text-text-placeholder"
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
            'flex items-center justify-between rounded-[2px] px-2 py-1.5 text-left text-sm text-text-hi outline-none transition-colors duration-[120ms]',
            'hover:bg-element focus:bg-element disabled:cursor-not-allowed disabled:opacity-50',
            modelValue === option.value && 'bg-element',
          ]"
          @click="choose(option)"
        >
          <span>{{ option.label }}</span>
          <svg
            v-if="modelValue === option.value"
            class="h-3 w-3 shrink-0 text-ac"
            viewBox="0 0 12 12"
            fill="none"
            aria-hidden="true"
          >
            <path
              d="M2 6L4.5 8.5L10 3"
              stroke="currentColor"
              stroke-width="1.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </button>
      </div>
    </div>
    <p v-if="error && isInvalid" class="font-mono text-xs text-err">{{ error }}</p>
    <p v-else-if="hint" class="font-mono text-xs text-text-placeholder">{{ hint }}</p>
  </div>
</template>
