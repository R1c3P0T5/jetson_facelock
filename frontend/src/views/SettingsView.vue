<script setup lang="ts">
import { State } from '@/lib'

defineOptions({ name: 'SettingsView' })
</script>

<template>
  <State title="Settings" variant="empty" :center="true" />
</template>
