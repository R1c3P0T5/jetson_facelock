<script setup lang="ts">
defineOptions({ name: 'UiNavItem' })

withDefaults(
  defineProps<{
    label: string
    href?: string
    active?: boolean
  }>(),
  {
    href: undefined,
    active: false,
  },
)

defineEmits<{
  click: [event: MouseEvent]
}>()
</script>

<template>
  <a
    :href="href"
    :class="[
      'grid cursor-pointer grid-cols-[6px_1fr] items-center gap-2.5 rounded-[2px] border px-2.5 py-2.5 font-mono text-[11px] uppercase tracking-[0.07em] no-underline transition-colors duration-[120ms]',
      'focus-visible:outline focus-visible:outline-1 focus-visible:outline-ac focus-visible:outline-offset-2',
      active
        ? 'border-border bg-element text-text-hi'
        : 'border-transparent text-text-lo hover:border-border hover:bg-overlay hover:text-text-hi',
    ]"
    :aria-current="active ? 'page' : undefined"
    @click="$emit('click', $event)"
  >
    <span
      :class="['h-1.5 w-1.5 rounded-full', active ? 'bg-ac' : 'bg-border']"
      aria-hidden="true"
    />
    {{ label }}
  </a>
</template>
