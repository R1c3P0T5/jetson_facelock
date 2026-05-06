<script setup lang="ts">
import Progress from './Progress.vue'

defineOptions({ name: 'ProgressStory' })
</script>

<template>
  <Story title="Progress" :layout="{ type: 'grid', width: 400 }">
    <Variant title="78%">
      <div class="grid gap-1.5">
        <Progress :value="78" label="Policy rollout" />
        <p class="font-mono text-xs text-text-placeholder">78% · 39 / 50 edge nodes updated</p>
      </div>
    </Variant>

    <Variant title="Full">
      <Progress :value="100" label="Sync complete" />
    </Variant>

    <Variant title="Zero">
      <Progress :value="0" label="Not started" />
    </Variant>

    <Variant title="Custom max">
      <Progress :value="3" :max="4" label="Steps" />
    </Variant>
  </Story>
</template>
