<script setup lang="ts">
import Button from './Button.vue'

defineOptions({
  name: 'UiButtonStory',
})
</script>

<template>
  <Story title="Button" :layout="{ type: 'grid', width: 160 }">
    <Variant title="Primary"><Button variant="primary">Primary</Button></Variant>
    <Variant title="Secondary"><Button variant="secondary">Secondary</Button></Variant>
    <Variant title="Outline"><Button variant="outline">Outline</Button></Variant>
    <Variant title="Ghost"><Button variant="ghost">Ghost</Button></Variant>
    <Variant title="Danger"><Button variant="danger">Danger</Button></Variant>
    <Variant title="Link"><Button variant="link">Link action</Button></Variant>
    <Variant title="XS"><Button size="xs">XS</Button></Variant>
    <Variant title="SM"><Button size="sm">SM</Button></Variant>
    <Variant title="LG"><Button size="lg">LG</Button></Variant>
    <Variant title="Loading"><Button :loading="true">Loading</Button></Variant>
    <Variant title="Disabled"><Button :disabled="true">Disabled</Button></Variant>
  </Story>
</template>
