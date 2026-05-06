<script setup lang="ts">
defineOptions({ name: 'UiAvatarStack' })
</script>

<template>
  <div class="flex [&>*]:-mr-2 [&>*]:border-2 [&>*]:border-bg">
    <slot />
  </div>
</template>
