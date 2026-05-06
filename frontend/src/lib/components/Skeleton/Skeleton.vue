<script setup lang="ts">
defineOptions({ name: 'UiSkeleton' })

const props = withDefaults(
  defineProps<{
    height?: string | number
    width?: string | number
  }>(),
  {
    height: 14,
    width: '100%',
  },
)

const toSize = (v: string | number) => (typeof v === 'number' ? `${v}px` : v)
</script>

<template>
  <div
    class="skeleton rounded-[2px] border border-border-soft"
    :style="{ height: toSize(props.height), width: toSize(props.width) }"
    role="status"
    aria-label="Loading"
  />
</template>

<style scoped>
.skeleton {
  background: linear-gradient(
    100deg,
    var(--color-element) 20%,
    var(--color-overlay) 45%,
    var(--color-element) 70%
  );
  background-size: 220% 100%;
  animation: shimmer 1.3s linear infinite;
}

@keyframes shimmer {
  to {
    background-position: -220% 0;
  }
}
</style>
