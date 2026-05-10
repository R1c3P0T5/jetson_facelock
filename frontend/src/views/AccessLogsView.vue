<script setup lang="ts">
import { State } from '@/lib'

defineOptions({ name: 'AccessLogsView' })
</script>

<template>
  <State title="Access Logs" variant="empty" :center="true" />
</template>
