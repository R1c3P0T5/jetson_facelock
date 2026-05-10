<script setup lang="ts">
import { State } from '@/lib'

defineOptions({ name: 'DashboardView' })
</script>

<template>
  <State title="Dashboard" variant="empty" :center="true" />
</template>
