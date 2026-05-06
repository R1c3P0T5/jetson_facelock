<script setup lang="ts">
import { ref, watch } from 'vue'

defineOptions({ name: 'UiAccordionItem' })

const props = withDefaults(
  defineProps<{
    title: string
    open?: boolean
  }>(),
  { open: false },
)

const emit = defineEmits<{
  'update:open': [value: boolean]
}>()

const isOpen = ref(props.open)
watch(
  () => props.open,
  (v) => (isOpen.value = v),
)

const toggle = () => {
  isOpen.value = !isOpen.value
  emit('update:open', isOpen.value)
}
</script>

<template>
  <div class="[&+&]:border-t [&+&]:border-border-soft">
    <button
      type="button"
      :aria-expanded="isOpen"
      class="flex w-full items-center justify-between bg-subtle px-3 py-2.5 font-mono text-xs uppercase tracking-[0.06em] text-text-hi transition-colors duration-[120ms] hover:bg-overlay focus-visible:outline focus-visible:outline-1 focus-visible:outline-ac focus-visible:outline-offset-[-1px]"
      @click="toggle"
    >
      <span>{{ title }}</span>
      <span
        class="shrink-0 text-text-placeholder transition-transform duration-[120ms]"
        :class="{ 'rotate-180': isOpen }"
        aria-hidden="true"
      >
        ▾
      </span>
    </button>
    <div
      v-show="isOpen"
      data-accordion-panel
      class="border-t border-border-soft bg-element px-3 py-3 text-sm text-text-lo"
    >
      <slot />
    </div>
  </div>
</template>
