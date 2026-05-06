<script setup lang="ts">
import { ref } from 'vue'

import Button from '../Button/Button.vue'
import Dialog from './Dialog.vue'

defineOptions({ name: 'DialogStory' })

const open = ref(false)
</script>

<template>
  <Story title="Overlay / Dialog" :layout="{ type: 'single', iframe: false }">
    <Variant title="Controlled">
      <Dialog v-model:open="open" title="Apply policy update?">
        <p>This action updates camera policy rules for all edge nodes.</p>
        <p>Estimated rollout: 45 seconds · 3 active nodes.</p>
        <template #footer>
          <Button variant="ghost" size="sm" @click="open = false">Cancel</Button>
          <Button variant="ok" size="sm" @click="open = false">Confirm update</Button>
        </template>
      </Dialog>
      <Button variant="secondary" size="sm" @click="open = true">Open dialog</Button>
    </Variant>
  </Story>
</template>
