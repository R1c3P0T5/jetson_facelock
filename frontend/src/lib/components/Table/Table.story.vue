<script setup lang="ts">
import { ref } from 'vue'

import Badge from '../Badge/Badge.vue'
import Pagination from './Pagination.vue'
import Table from './Table.vue'
import type { SortDir } from './Table.vue'

defineOptions({ name: 'TableStory' })

const columns = [
  { key: 'ts', label: 'Timestamp', sortable: true },
  { key: 'identity', label: 'Identity', sortable: true },
  { key: 'result', label: 'Result' },
  { key: 'confidence', label: 'Confidence', sortable: true },
  { key: 'camera', label: 'Camera' },
  { key: 'latency', label: 'Latency', sortable: true },
]

const rows = [
  {
    ts: '14:41:18',
    identity: '張小明',
    result: 'ok',
    confidence: '98.4%',
    camera: 'CAM-01',
    latency: '11ms',
  },
  {
    ts: '14:40:31',
    identity: 'Unknown',
    result: 'err',
    confidence: '—',
    camera: 'CAM-02',
    latency: '14ms',
  },
  {
    ts: '14:38:47',
    identity: '王建志',
    result: 'ok',
    confidence: '97.9%',
    camera: 'CAM-03',
    latency: '12ms',
  },
  {
    ts: '14:37:12',
    identity: '李雨蓁',
    result: 'ok',
    confidence: '96.7%',
    camera: 'CAM-01',
    latency: '13ms',
  },
]

const sortKey = ref('ts')
const sortDir = ref<SortDir>('asc')
const page = ref(1)

const resultVariant = (v: unknown): 'ok' | 'err' => (v === 'ok' ? 'ok' : 'err')
</script>

<template>
  <Story title="Data / Table" :layout="{ type: 'single', iframe: false }">
    <Variant title="With sort + pagination">
      <div class="grid gap-3">
        <Table
          :columns="columns"
          :rows="rows"
          :sort-key="sortKey"
          :sort-dir="sortDir"
          @sort="
            (k, d) => {
              sortKey = k
              sortDir = d
            }
          "
        >
          <template #cell-result="{ value }">
            <Badge :variant="resultVariant(value)">{{
              value === 'ok' ? 'Granted' : 'Denied'
            }}</Badge>
          </template>
        </Table>
        <Pagination v-model:page="page" :page-size="10" :total="128" />
      </div>
    </Variant>
  </Story>
</template>
