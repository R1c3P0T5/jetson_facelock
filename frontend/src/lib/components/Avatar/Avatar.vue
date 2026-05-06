<script setup lang="ts">
defineOptions({ name: 'UiAvatar' })

export type AvatarSize = 'sm' | 'md' | 'lg'

withDefaults(
  defineProps<{
    initials: string
    src?: string
    size?: AvatarSize
  }>(),
  {
    src: undefined,
    size: 'md',
  },
)

const sizeClasses: Record<AvatarSize, string> = {
  sm: 'h-6 w-6 text-[10px]',
  md: 'h-7.5 w-7.5 text-xs',
  lg: 'h-10 w-10 text-sm',
}
</script>

<template>
  <span
    :class="[
      'relative inline-flex shrink-0 items-center justify-center overflow-hidden rounded-full border border-border bg-element font-mono tracking-[0.04em] text-text-hi',
      sizeClasses[size],
    ]"
  >
    <img v-if="src" :src="src" :alt="initials" class="h-full w-full object-cover" />
    <span v-else aria-hidden="true">{{ initials }}</span>
  </span>
</template>
