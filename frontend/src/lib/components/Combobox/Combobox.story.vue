<script setup lang="ts">
import { ref } from 'vue'

import Combobox, { type ComboboxOption } from './Combobox.vue'

defineOptions({
  name: 'UiComboboxStory',
})

const door = ref('garage')
const emptyDoor = ref('')
const disabledDoor = ref('front-door')

const doors: ComboboxOption[] = [
  { value: 'front-door', label: 'Front door' },
  { value: 'garage', label: 'Garage' },
  { value: 'server-room', label: 'Server room', disabled: true },
]
</script>

<template>
  <Story title="Combobox" :layout="{ type: 'grid', width: 340 }">
    <Variant title="Default">
      <Combobox v-model="door" :options="doors" />
    </Variant>
    <Variant title="Placeholder">
      <Combobox v-model="emptyDoor" placeholder="Search door" :options="doors" />
    </Variant>
    <Variant title="Invalid">
      <Combobox
        v-model="emptyDoor"
        invalid
        error="Door is required."
        placeholder="Search door"
        :options="doors"
      />
    </Variant>
    <Variant title="Disabled">
      <Combobox v-model="disabledDoor" disabled :options="doors" />
    </Variant>
  </Story>
</template>
