<script setup lang="ts">
import Menu from './Menu.vue'
import MenuItem from './MenuItem.vue'
import MenuSeparator from './MenuSeparator.vue'

defineOptions({ name: 'MenuStory' })
</script>

<template>
  <Story title="Menu" :layout="{ type: 'grid', width: 280 }">
    <Variant title="Default">
      <Menu>
        <MenuItem label="Open in timeline" />
        <MenuItem label="Mark as reviewed" />
        <MenuSeparator />
        <MenuItem label="Create incident" />
        <MenuItem label="Download snapshot" />
      </Menu>
    </Variant>

    <Variant title="With destructive item">
      <Menu>
        <MenuItem label="Edit policy" />
        <MenuItem label="Duplicate" />
        <MenuSeparator />
        <MenuItem label="Delete policy" :destructive="true" />
      </Menu>
    </Variant>

    <Variant title="With disabled item">
      <Menu>
        <MenuItem label="Export report" />
        <MenuItem label="Archive (offline)" :disabled="true" />
        <MenuItem label="Share link" />
      </Menu>
    </Variant>
  </Story>
</template>
