<script setup lang="ts">
defineOptions({ name: 'UiToast' })

import { useToast } from './useToast'

const { toasts, hide } = useToast()
</script>

<template>
  <Teleport to="body">
    <TransitionGroup
      tag="div"
      class="fixed bottom-3.5 right-3.5 z-[75] flex flex-col items-end gap-2"
      enter-active-class="transition-all duration-[140ms]"
      enter-from-class="translate-y-3 opacity-0"
      leave-active-class="transition-all duration-[140ms]"
      leave-to-class="translate-y-3 opacity-0"
    >
      <div
        v-for="toast in toasts"
        :key="toast.id"
        role="status"
        aria-live="polite"
        class="min-w-80 cursor-pointer rounded-[2px] border border-l-2 border-border border-l-ac bg-subtle px-3 py-2.5 text-text-hi"
        @click="hide(toast.id)"
      >
        <strong class="font-mono text-xs uppercase tracking-[0.06em]">{{ toast.title }}</strong>
        <p v-if="toast.message" class="mt-0.5 text-sm text-text-lo">{{ toast.message }}</p>
      </div>
    </TransitionGroup>
  </Teleport>
</template>
