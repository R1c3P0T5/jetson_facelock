<script setup lang="ts">
defineOptions({ name: 'UiEmpty' })

defineProps<{
  title: string
  description?: string
}>()
</script>

<template>
  <div
    class="flex min-h-[200px] flex-col items-center justify-center gap-4 rounded-[2px] border border-dashed border-border p-10 text-center"
  >
    <div
      v-if="$slots.icon"
      class="text-text-placeholder [&>svg]:h-8 [&>svg]:w-8 [&>svg]:opacity-40"
    >
      <slot name="icon" />
    </div>
    <div class="grid gap-1.5">
      <h3 class="font-mono text-sm uppercase tracking-[0.08em] text-text-hi">{{ title }}</h3>
      <p
        v-if="description"
        data-empty-description
        class="mx-auto max-w-[40ch] text-sm text-text-placeholder"
      >
        {{ description }}
      </p>
    </div>
    <slot />
  </div>
</template>
