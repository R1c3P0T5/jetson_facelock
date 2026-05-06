<script setup lang="ts">
defineOptions({ name: 'UiMenuItem' })

const props = withDefaults(
  defineProps<{
    label: string
    disabled?: boolean
    destructive?: boolean
  }>(),
  {
    disabled: false,
    destructive: false,
  },
)

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const handleClick = (event: MouseEvent) => {
  if (!props.disabled) emit('click', event)
}
</script>

<template>
  <button
    type="button"
    role="menuitem"
    :disabled="props.disabled"
    :class="[
      'w-full rounded-[2px] border border-transparent px-2.5 py-2 text-left font-mono text-xs uppercase tracking-[0.05em] transition-colors duration-[120ms]',
      'focus-visible:outline focus-visible:outline-1 focus-visible:outline-ac focus-visible:outline-offset-1',
      props.disabled && 'cursor-not-allowed opacity-50',
      !props.disabled && props.destructive && 'text-err hover:border-err/30 hover:bg-err/10',
      !props.disabled &&
        !props.destructive &&
        'text-text-lo hover:border-border hover:bg-overlay hover:text-text-hi',
    ]"
    @click="handleClick"
  >
    <span v-if="$slots.icon" class="mr-2 inline-flex text-current opacity-60">
      <slot name="icon" />
    </span>
    {{ props.label }}
    <span v-if="$slots.trailing" class="float-right text-text-placeholder">
      <slot name="trailing" />
    </span>
  </button>
</template>
