<script setup lang="ts">
defineOptions({ name: 'UiPlaceholder' })

withDefaults(
  defineProps<{
    width?: string | number
    height?: string | number
    label?: string
  }>(),
  {
    width: '100%',
    height: 120,
  },
)

const toSize = (v: string | number) => (typeof v === 'number' ? `${v}px` : v)
</script>

<template>
  <div
    class="placeholder"
    :style="{ width: toSize(width), height: toSize(height) }"
    role="img"
    :aria-label="label ?? 'Placeholder'"
  >
    <svg class="hatch" aria-hidden="true">
      <defs>
        <pattern
          id="hatch"
          width="10"
          height="10"
          patternUnits="userSpaceOnUse"
          patternTransform="rotate(-45)"
        >
          <line x1="0" y1="0" x2="0" y2="10" class="hatch-line" />
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill="url(#hatch)" />
    </svg>
    <span v-if="label" class="label">{{ label }}</span>
  </div>
</template>

<style scoped>
.placeholder {
  position: relative;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  overflow: hidden;
  background-color: var(--color-element);
}

.hatch {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.hatch-line {
  stroke: var(--color-border-soft);
  stroke-width: 1;
}

.label {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  color: var(--color-text-placeholder);
  background: color-mix(in srgb, var(--color-element) 70%, transparent);
  padding: 0.25rem 0.5rem;
  text-align: center;
}
</style>
