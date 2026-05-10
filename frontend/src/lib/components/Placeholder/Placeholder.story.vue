<script setup lang="ts">
import Placeholder from './Placeholder.vue'

defineOptions({ name: 'PlaceholderStory' })
</script>

<template>
  <Story title="Util / Placeholder" :layout="{ type: 'grid', width: 400 }">
    <Variant title="Default">
      <Placeholder />
    </Variant>

    <Variant title="With label">
      <Placeholder label="Chart" />
    </Variant>

    <Variant title="Small">
      <Placeholder :height="48" label="Icon" />
    </Variant>

    <Variant title="Custom size">
      <Placeholder width="200px" :height="200" label="Image" />
    </Variant>

    <Variant title="Full width tall">
      <Placeholder :height="240" label="Map" />
    </Variant>

    <Variant title="Layout composition">
      <div class="grid gap-3">
        <Placeholder :height="160" label="Hero" />
        <div class="grid grid-cols-2 gap-3">
          <Placeholder :height="80" label="Card A" />
          <Placeholder :height="80" label="Card B" />
        </div>
      </div>
    </Variant>
  </Story>
</template>
