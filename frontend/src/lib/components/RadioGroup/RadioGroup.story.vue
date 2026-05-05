<script setup lang="ts">
import { ref } from 'vue'

import RadioGroup, { type RadioGroupOption } from './RadioGroup.vue'

defineOptions({
  name: 'UiRadioGroupStory',
})

const unlockMethod = ref('face')
const camera = ref('front')
const disabledValue = ref('card')

const methods: RadioGroupOption[] = [
  { value: 'pin', label: 'PIN' },
  { value: 'face', label: 'Face unlock', description: 'Use camera verification.' },
  { value: 'card', label: 'Access card', disabled: true },
]

const cameras: RadioGroupOption[] = [
  { value: 'front', label: 'Front' },
  { value: 'side', label: 'Side' },
  { value: 'rear', label: 'Rear' },
]
</script>

<template>
  <Story title="RadioGroup" :layout="{ type: 'grid', width: 340 }">
    <Variant title="Default">
      <RadioGroup v-model="unlockMethod" name="unlock-method" :options="methods" />
    </Variant>
    <Variant title="Horizontal">
      <RadioGroup
        v-model="camera"
        name="camera-position"
        :options="cameras"
        orientation="horizontal"
      />
    </Variant>
    <Variant title="Disabled">
      <RadioGroup v-model="disabledValue" disabled name="disabled-method" :options="methods" />
    </Variant>
    <Variant title="Invalid">
      <RadioGroup model-value="" invalid name="invalid-method" :options="methods" />
    </Variant>
  </Story>
</template>
