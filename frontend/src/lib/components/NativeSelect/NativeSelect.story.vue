<script setup lang="ts">
import { ref } from 'vue'

import NativeSelect, { type NativeSelectOption } from './NativeSelect.vue'

defineOptions({
  name: 'UiNativeSelectStory',
})

const role = ref('owner')
const emptyRole = ref('')
const policyRole = ref('guest')

const roles: NativeSelectOption[] = [
  { value: 'owner', label: 'Owner' },
  { value: 'guest', label: 'Guest' },
  { value: 'locked', label: 'Locked', disabled: true },
]
</script>

<template>
  <Story title="Form / Native Select" :layout="{ type: 'grid', width: 320 }">
    <Variant title="Default">
      <NativeSelect v-model="role" :options="roles" />
    </Variant>
    <Variant title="Placeholder">
      <NativeSelect v-model="emptyRole" placeholder="Choose role" :options="roles" />
    </Variant>
    <Variant title="Invalid">
      <NativeSelect
        v-model="emptyRole"
        invalid
        error="Role is required."
        placeholder="Choose role"
        :options="roles"
      />
    </Variant>
    <Variant title="Disabled">
      <NativeSelect v-model="policyRole" disabled :options="roles" />
    </Variant>
  </Story>
</template>
