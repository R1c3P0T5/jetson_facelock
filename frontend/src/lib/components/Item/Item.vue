<script setup lang="ts">
defineOptions({ name: 'UiItem' })

withDefaults(
  defineProps<{
    label: string
    description?: string
    interactive?: boolean
    disabled?: boolean
  }>(),
  {
    description: undefined,
    interactive: false,
    disabled: false,
  },
)

defineEmits<{
  click: [event: MouseEvent]
}>()
</script>

<template>
  <div
    :class="[
      'flex min-w-0 items-center gap-3 rounded-[2px] px-2.5 py-2',
      interactive &&
        !disabled &&
        'cursor-pointer hover:bg-overlay transition-colors duration-[120ms]',
      disabled && 'cursor-not-allowed opacity-50',
    ]"
    @click="!disabled && $emit('click', $event)"
  >
    <span v-if="$slots.icon" class="shrink-0 text-text-placeholder [&>*]:h-4 [&>*]:w-4">
      <slot name="icon" />
    </span>
    <div class="grid min-w-0 flex-1 gap-0.5">
      <span class="truncate text-sm text-text-hi">{{ label }}</span>
      <span
        v-if="description"
        data-item-description
        class="truncate font-mono text-xs text-text-placeholder"
      >
        {{ description }}
      </span>
    </div>
    <span v-if="$slots.trailing" class="shrink-0 text-text-placeholder">
      <slot name="trailing" />
    </span>
  </div>
</template>
