<script setup lang="ts">
import Skeleton from './Skeleton.vue'

defineOptions({ name: 'SkeletonStory' })
</script>

<template>
  <Story title="Skeleton" :layout="{ type: 'grid', width: 400 }">
    <Variant title="Default (text line)">
      <Skeleton />
    </Variant>

    <Variant title="Tall block">
      <Skeleton :height="88" />
    </Variant>

    <Variant title="Custom width">
      <Skeleton :height="14" width="60%" />
    </Variant>

    <Variant title="Loading list">
      <div class="grid gap-2">
        <Skeleton />
        <Skeleton width="75%" />
        <Skeleton :height="88" />
      </div>
    </Variant>
  </Story>
</template>
