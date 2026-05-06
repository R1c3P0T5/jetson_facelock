<script setup lang="ts">
import Badge from '../Badge/Badge.vue'
import Card from './Card.vue'

defineOptions({ name: 'CardStory' })
</script>

<template>
  <Story title="Card" :layout="{ type: 'grid', width: 480 }">
    <Variant title="Body only">
      <Card>
        <p class="text-sm text-text-lo">Plain card with no header — just a bordered surface.</p>
      </Card>
    </Variant>

    <Variant title="With kicker + title">
      <Card kicker="Data display" title="Access log">
        <p class="text-sm text-text-lo">Table or content goes here.</p>
      </Card>
    </Variant>

    <Variant title="With action slot">
      <Card kicker="Quick stats" title="Metric cards">
        <template #action>
          <Badge variant="ok">Streaming</Badge>
        </template>
        <p class="text-sm text-text-lo">Metric grid goes here.</p>
      </Card>
    </Variant>
  </Story>
</template>
