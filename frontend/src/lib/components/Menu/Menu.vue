<script setup lang="ts">
defineOptions({ name: 'UiMenu' })
</script>

<template>
  <div
    class="w-min-[200px] grid gap-1 rounded-[2px] border border-border bg-subtle p-1.5"
    role="menu"
  >
    <slot />
  </div>
</template>
