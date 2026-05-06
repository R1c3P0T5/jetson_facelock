<script setup lang="ts">
import Button from '../Button/Button.vue'
import State from './State.vue'

defineOptions({ name: 'StateStory' })
</script>

<template>
  <Story title="State" :layout="{ type: 'grid', width: 400 }">
    <Variant title="Empty (left-aligned)">
      <State title="No matched record">
        <p class="text-sm">Try another sample or refine camera angle.</p>
        <Button variant="secondary" size="sm">Scan again</Button>
      </State>
    </Variant>

    <Variant title="Empty (centered)">
      <State title="No critical alerts" center>
        <p class="text-sm">Last severity=high incident closed 2h ago.</p>
      </State>
    </Variant>

    <Variant title="Error (centered)">
      <State title="Audit stream interrupted" variant="error" center>
        <p class="text-sm">Collector endpoint timeout. Retry with backoff.</p>
        <Button variant="err" size="sm">Retry sync</Button>
      </State>
    </Variant>
  </Story>
</template>
