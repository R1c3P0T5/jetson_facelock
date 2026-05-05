<script setup lang="ts">
defineOptions({ name: 'UiTabs' })

export interface Tab {
  key: string
  label: string
}

defineProps<{
  tabs: Tab[]
  modelValue: string
}>()

const emit = defineEmits<{
  'update:modelValue': [key: string]
}>()
</script>

<template>
  <div>
    <div role="tablist" class="mb-2.5 flex flex-wrap gap-2 border-b border-border-soft pb-2.5">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        role="tab"
        :aria-selected="modelValue === tab.key"
        :class="[
          'cursor-pointer rounded-[2px] border px-2.5 py-2 font-mono text-xs uppercase tracking-[0.06em] transition-colors duration-[120ms]',
          'focus-visible:outline focus-visible:outline-1 focus-visible:outline-ac focus-visible:outline-offset-2',
          modelValue === tab.key
            ? 'border-ac bg-element text-text-hi'
            : 'border-border bg-transparent text-text-lo hover:bg-element hover:text-text-hi',
        ]"
        @click="emit('update:modelValue', tab.key)"
      >
        {{ tab.label }}
      </button>
    </div>
    <div role="tabpanel">
      <slot :name="modelValue" />
    </div>
  </div>
</template>
