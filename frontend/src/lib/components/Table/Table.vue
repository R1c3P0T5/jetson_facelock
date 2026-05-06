<script setup lang="ts">
defineOptions({ name: 'UiTable' })

export interface TableColumn {
  key: string
  label: string
  sortable?: boolean
}

export type SortDir = 'asc' | 'desc'

const props = defineProps<{
  columns: TableColumn[]
  rows: Record<string, unknown>[]
  sortKey?: string
  sortDir?: SortDir
}>()

const emit = defineEmits<{
  sort: [key: string, dir: SortDir]
}>()

const handleSort = (col: TableColumn) => {
  if (!col.sortable) return
  const newDir: SortDir = props.sortKey === col.key && props.sortDir === 'asc' ? 'desc' : 'asc'
  emit('sort', col.key, newDir)
}
</script>

<template>
  <div class="overflow-x-auto">
    <table class="w-full border-collapse">
      <thead>
        <tr>
          <th
            v-for="col in columns"
            :key="col.key"
            class="border-b border-border px-2 py-2.5 text-left font-mono text-[11px] uppercase tracking-[0.1em] whitespace-nowrap text-text-placeholder"
          >
            <button
              v-if="col.sortable"
              data-sort-btn
              type="button"
              class="inline-flex items-center gap-1 hover:text-text-lo transition-colors"
              @click="handleSort(col)"
            >
              {{ col.label }}
              <span aria-hidden="true" class="text-[10px] opacity-60">
                {{ sortKey === col.key ? (sortDir === 'asc' ? '↑' : '↓') : '↕' }}
              </span>
            </button>
            <span v-else>{{ col.label }}</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, ri) in rows" :key="ri" class="group transition-colors hover:bg-overlay">
          <td
            v-for="col in columns"
            :key="col.key"
            class="border-b border-border-soft px-2 py-2.5 text-sm tabular-nums text-text-lo group-last:border-b-0"
          >
            <slot :name="`cell-${col.key}`" :row="row" :value="row[col.key]">
              {{ row[col.key] }}
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
