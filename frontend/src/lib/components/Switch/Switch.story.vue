<script setup lang="ts">
import { ref } from 'vue'

import Switch from './Switch.vue'

defineOptions({
  name: 'UiSwitchStory',
})

const on = ref(true)
const off = ref(false)
const disabled = ref(true)
</script>

<template>
  <Story title="Switch" :layout="{ type: 'grid', width: 220 }">
    <Variant title="On">
      <Switch v-model="on" label="Realtime mode" />
    </Variant>
    <Variant title="Off">
      <Switch v-model="off" label="Auto quarantine" />
    </Variant>
    <Variant title="Disabled">
      <Switch v-model="disabled" label="Locked policy" disabled />
    </Variant>
  </Story>
</template>
