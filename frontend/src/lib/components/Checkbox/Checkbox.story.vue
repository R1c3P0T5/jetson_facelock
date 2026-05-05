<script setup lang="ts">
import { ref } from 'vue'

import Checkbox from './Checkbox.vue'

defineOptions({
  name: 'UiCheckboxStory',
})

const device = ref(true)
const updates = ref(false)
const policy = ref(true)
</script>

<template>
  <Story title="Checkbox" :layout="{ type: 'grid', width: 280 }">
    <Variant title="Checked">
      <Checkbox v-model="device" label="Remember this device" />
    </Variant>
    <Variant title="Unchecked">
      <Checkbox v-model="updates" label="Email me updates" />
    </Variant>
    <Variant title="Description">
      <Checkbox
        v-model="device"
        label="Trust this browser"
        description="Skip approval prompts on this device."
      />
    </Variant>
    <Variant title="Disabled">
      <Checkbox v-model="policy" disabled label="Managed by policy" />
    </Variant>
    <Variant title="Invalid">
      <Checkbox :model-value="false" invalid label="Required approval" />
    </Variant>
  </Story>
</template>
