<script setup lang="ts">
import Metric from './Metric.vue'

defineOptions({ name: 'MetricStory' })
</script>

<template>
  <Story title="Metric" :layout="{ type: 'grid', width: 480 }">
    <Variant title="Grid (2-col)">
      <div class="grid grid-cols-2 gap-2.5">
        <Metric label="Today scans" value="1,284" delta="+3.1% vs yesterday" />
        <Metric label="Grant rate" value="97.2%" delta="Within target" />
        <Metric label="Denied events" value="36" delta="12 pending review" />
        <Metric label="Latency p95" value="12ms" delta="Edge runtime" />
      </div>
    </Variant>

    <Variant title="Single">
      <Metric label="Active nodes" value="50" />
    </Variant>
  </Story>
</template>
