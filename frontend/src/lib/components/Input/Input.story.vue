<script setup lang="ts">
import { ref } from 'vue'

import Input from './Input.vue'

defineOptions({
  name: 'UiInputStory',
})

const value = ref('FG-0138')
const empty = ref('')
const invalid = ref('bad value')
const search = ref('')
</script>

<template>
  <Story title="Form / Input" :layout="{ type: 'grid', width: 280 }">
    <Variant title="Default">
      <Input v-model="empty" placeholder="Device ID" />
    </Variant>
    <Variant title="Required">
      <Input
        v-model="empty"
        required
        placeholder="Required field"
        hint="This field must be filled out."
      />
    </Variant>
    <Variant title="Search">
      <Input v-model="search" type="search" placeholder="Search..." />
    </Variant>
    <Variant title="With prefix">
      <Input v-model="value" prefix="#" hint="ID must map to registry profile." />
    </Variant>
    <Variant title="With suffix">
      <Input v-model="value" suffix="%" />
    </Variant>
    <Variant title="Invalid">
      <Input
        v-model="invalid"
        :invalid="true"
        error="Attach reviewer decision before continuing."
      />
    </Variant>
    <Variant title="Disabled">
      <Input
        v-model="empty"
        disabled
        placeholder="Email"
        hint="This field is currently disabled."
      />
    </Variant>
    <Variant title="File">
      <Input :model-value="''" type="file" hint="Select a picture to upload." />
    </Variant>
  </Story>
</template>
