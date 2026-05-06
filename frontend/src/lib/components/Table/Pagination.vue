<script setup lang="ts">
import { computed } from 'vue'

defineOptions({ name: 'UiPagination' })

const props = defineProps<{
  page: number
  pageSize: number
  total: number
}>()

const emit = defineEmits<{
  'update:page': [page: number]
}>()

const totalPages = computed(() => Math.ceil(props.total / props.pageSize))
const start = computed(() => (props.page - 1) * props.pageSize + 1)
const end = computed(() => Math.min(props.page * props.pageSize, props.total))

const visiblePages = computed(() => {
  const pages: number[] = []
  for (let i = Math.max(1, props.page - 1); i <= Math.min(totalPages.value, props.page + 1); i++) {
    pages.push(i)
  }
  return pages
})
</script>

<template>
  <div class="flex flex-wrap items-center justify-between gap-2.5">
    <span class="font-mono text-xs text-text-placeholder">
      {{ start }}–{{ end }} of {{ total }}
    </span>
    <div class="flex items-center gap-1">
      <button
        data-prev
        type="button"
        :disabled="page <= 1"
        class="rounded-[2px] border border-border bg-element px-2.5 py-1.5 font-mono text-xs text-text-lo transition-colors hover:border-text-placeholder hover:text-text-hi disabled:cursor-not-allowed disabled:opacity-40"
        @click="emit('update:page', page - 1)"
      >
        Prev
      </button>
      <button
        v-for="p in visiblePages"
        :key="p"
        type="button"
        :class="[
          'rounded-[2px] border px-2.5 py-1.5 font-mono text-xs transition-colors',
          p === page
            ? 'border-ac bg-ac/10 text-ac'
            : 'border-border bg-element text-text-lo hover:border-text-placeholder hover:text-text-hi',
        ]"
        @click="emit('update:page', p)"
      >
        {{ p }}
      </button>
      <button
        data-next
        type="button"
        :disabled="page >= totalPages"
        class="rounded-[2px] border border-border bg-element px-2.5 py-1.5 font-mono text-xs text-text-lo transition-colors hover:border-text-placeholder hover:text-text-hi disabled:cursor-not-allowed disabled:opacity-40"
        @click="emit('update:page', page + 1)"
      >
        Next
      </button>
    </div>
  </div>
</template>
