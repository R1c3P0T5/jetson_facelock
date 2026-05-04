<script setup lang="ts">
import { computed } from 'vue'

export type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'link'
export type ButtonSize = 'xs' | 'sm' | 'default' | 'lg' | 'icon'

defineOptions({
  name: 'UiButton',
})

const props = withDefaults(
  defineProps<{
    variant?: ButtonVariant
    size?: ButtonSize
    loading?: boolean
    disabled?: boolean
  }>(),
  {
    variant: 'secondary',
    size: 'default',
    loading: false,
    disabled: false,
  },
)

const base =
  'inline-flex items-center justify-center gap-1.5 rounded-[2px] border font-mono text-xs uppercase tracking-[0.06em] whitespace-nowrap transition-all duration-[120ms] cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed focus-visible:outline focus-visible:outline-1 focus-visible:outline-ac focus-visible:outline-offset-2'

const sizeClasses: Record<ButtonSize, string> = {
  xs: 'min-h-[30px] px-2.5 py-1.5 text-[11px]',
  sm: 'min-h-[34px] px-3 py-2',
  default: 'min-h-[36px] px-3 py-2',
  lg: 'min-h-[42px] px-3.5 py-2.5 text-[13px]',
  icon: 'min-h-[36px] w-[36px] p-0',
}

const variantClasses: Record<ButtonVariant, string> = {
  primary: 'bg-ac border-ac text-bg hover:bg-text-hi hover:border-text-hi',
  secondary: 'bg-element border-border text-text-hi hover:border-text-placeholder',
  outline:
    'border-text-placeholder text-text-hi bg-transparent hover:bg-overlay hover:border-text-lo',
  ghost:
    'border-transparent text-text-lo bg-transparent hover:bg-overlay hover:border-border hover:text-text-hi',
  danger: 'text-err border-err/50 bg-err/12 hover:bg-err/20 hover:border-err',
  link: 'border-transparent bg-transparent text-ac underline p-0 min-h-0 hover:opacity-75',
}

const classes = computed(() => [base, sizeClasses[props.size], variantClasses[props.variant]])
</script>

<template>
  <button
    v-bind="$attrs"
    :class="classes"
    :disabled="disabled || loading"
    :aria-busy="loading || undefined"
  >
    <slot />
    <span v-if="loading" class="loading-spinner" aria-hidden="true" />
  </button>
</template>

<style scoped>
.loading-spinner {
  width: 10px;
  height: 10px;
  border: 1px solid color-mix(in srgb, currentColor 45%, transparent);
  border-top-color: currentColor;
  border-radius: 999px;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(1turn);
  }
}
</style>
