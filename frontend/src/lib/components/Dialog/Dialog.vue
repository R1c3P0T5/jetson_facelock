<script setup lang="ts">
defineOptions({ name: 'UiDialog' })

defineProps<{
  open: boolean
  title: string
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
}>()
</script>

<template>
  <Teleport to="body">
    <div
      v-if="open"
      data-backdrop
      class="fixed inset-0 z-[80] flex items-center justify-center bg-black/40 p-4"
      @click.self="emit('update:open', false)"
    >
      <div
        role="dialog"
        aria-modal="true"
        :aria-labelledby="`dialog-title-${title}`"
        class="mx-auto w-full max-w-[560px] rounded-[2px] border border-border bg-bg/85 shadow-2xl backdrop-blur-md [--tw-inset-shadow:inset_0_1px_0_rgba(255,255,255,0.06),inset_0_-1px_0_rgba(0,0,0,0.12)]"
      >
        <div class="flex items-center gap-2 border-b border-border-soft px-3.5 py-3">
          <h2
            :id="`dialog-title-${title}`"
            class="font-mono text-sm uppercase tracking-[0.05em] text-text-hi"
          >
            {{ title }}
          </h2>
        </div>
        <div class="grid gap-2 p-3.5 text-sm text-text-lo">
          <slot />
        </div>
        <div
          v-if="$slots.footer"
          class="flex justify-end gap-2 border-t border-border-soft px-3.5 py-2.5"
        >
          <slot name="footer" />
        </div>
      </div>
    </div>
  </Teleport>
</template>
