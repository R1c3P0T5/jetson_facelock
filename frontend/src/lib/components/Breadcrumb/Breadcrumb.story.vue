<script setup lang="ts">
import Breadcrumb from './Breadcrumb.vue'

defineOptions({ name: 'BreadcrumbStory' })

const items = [{ label: 'ops' }, { label: 'access-control', href: '/access' }, { label: 'policy' }]
</script>

<template>
  <Story title="Navigation / Breadcrumb" :layout="{ type: 'single', iframe: false }">
    <Variant title="Default">
      <Breadcrumb :items="items" />
    </Variant>

    <Variant title="Short path">
      <Breadcrumb :items="[{ label: 'settings' }, { label: 'cameras' }]" />
    </Variant>
  </Story>
</template>
