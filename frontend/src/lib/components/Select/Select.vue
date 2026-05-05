<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, useAttrs } from 'vue'

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
const root = ref<HTMLElement>()
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
      <button
        v-bind="$attrs"
        type="button"
        aria-haspopup="listbox"
        :aria-expanded="open ? 'true' : 'false'"
        :aria-invalid="isInvalid || undefined"
        :disabled="disabled"
        :class="[
          'flex min-h-9.5 w-full items-center justify-between gap-2 rounded-[2px] border bg-bg px-2.5 py-2 text-left font-sans text-sm outline-none transition-colors duration-[120ms]',
          'disabled:cursor-not-allowed disabled:opacity-50',
          'focus:border-ac focus:ring-1 focus:ring-ac/20',
          selectedOption ? 'text-text-hi' : 'text-text-placeholder',
          isInvalid ? 'border-err focus:ring-err/20' : 'border-border',
        ]"
        @click="toggle"
        @keydown.escape.prevent="close"
      >
        <span>{{ selectedOption?.label ?? placeholder }}</span>
        <svg
          :class="[
            'h-3 w-3 shrink-0 text-text-placeholder transition-transform duration-[120ms]',
            open && 'rotate-180',
          ]"
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
      </button>
      <div
        v-if="open"
        role="listbox"
        class="absolute left-0 right-0 top-full z-20 mt-1 grid max-h-56 overflow-auto rounded-[2px] border border-border bg-overlay p-1 shadow-lg"
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
