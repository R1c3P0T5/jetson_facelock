<script setup lang="ts">
import Badge from './Badge.vue'

defineOptions({
  name: 'UiBadgeStory',
})
</script>

<template>
  <Story title="Primitives / Badge" :layout="{ type: 'grid', width: 120 }">
    <Variant title="Ok"><Badge variant="ok">Granted</Badge></Variant>
    <Variant title="Info"><Badge variant="info">Synced</Badge></Variant>
    <Variant title="Warn"><Badge variant="warn">Review</Badge></Variant>
    <Variant title="Err"><Badge variant="err">Denied</Badge></Variant>
    <Variant title="Dim"><Badge variant="dim">Draft</Badge></Variant>
    <Variant title="Custom"><Badge color="#326f91">Camera</Badge></Variant>
    <Variant title="With dot">
      <Badge variant="info">
        <span class="w-1.5 h-1.5 rounded-full bg-current opacity-80" aria-hidden="true" />
        Online
      </Badge>
    </Variant>
  </Story>
</template>
