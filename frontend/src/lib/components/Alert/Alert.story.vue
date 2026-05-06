<script setup lang="ts">
import Alert from './Alert.vue'

defineOptions({
  name: 'UiAlertStory',
})
</script>

<template>
  <Story title="Primitives / Alert" :layout="{ type: 'single', iframe: false }">
    <Variant title="Ok">
      <Alert variant="ok" title="Stream healthy"
        >All capture nodes synced in last 30 seconds.</Alert
      >
    </Variant>
    <Variant title="Info">
      <Alert variant="info" title="Model updated"
        >Face embedding index refreshed from latest enrollment.</Alert
      >
    </Variant>
    <Variant title="With icon">
      <Alert variant="info" title="Model updated">
        <template #icon>
          <span class="font-mono text-xs" aria-hidden="true">i</span>
        </template>
        Face embedding index refreshed from latest enrollment.
      </Alert>
    </Variant>
    <Variant title="Warn">
      <Alert variant="warn" title="Queue elevated"
        >CAM-03 backlog exceeded baseline threshold.</Alert
      >
    </Variant>
    <Variant title="Err">
      <Alert variant="err" title="Policy failure">Signature validation timeout on edge-7.</Alert>
    </Variant>
    <Variant title="Dim">
      <Alert variant="dim" title="Muted source"
        >Lobby camera is excluded from unlock decisions.</Alert
      >
    </Variant>
    <Variant title="Body only">
      <Alert variant="dim">Lobby camera is excluded from unlock decisions.</Alert>
    </Variant>
    <Variant title="Closable">
      <Alert variant="warn" title="Queue elevated" closable
        >CAM-03 backlog exceeded baseline threshold.</Alert
      >
    </Variant>
  </Story>
</template>
