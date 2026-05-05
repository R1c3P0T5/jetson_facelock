<script setup lang="ts">
import { ref } from 'vue'

import Textarea from './Textarea.vue'

defineOptions({
  name: 'UiTextareaStory',
})

const notes = ref('Lobby camera is temporarily disabled.')
const empty = ref('')
const policy = ref('Only owners can edit this note.')
</script>

<template>
  <Story title="Textarea" :layout="{ type: 'grid', width: 360 }">
    <Variant title="Default">
      <Textarea v-model="notes" placeholder="Add device notes" />
    </Variant>
    <Variant title="Hint">
      <Textarea v-model="empty" hint="Visible to administrators only." placeholder="Add reason" />
    </Variant>
    <Variant title="Invalid">
      <Textarea
        v-model="empty"
        invalid
        error="Reason is required."
        placeholder="Why is access denied?"
      />
    </Variant>
    <Variant title="Disabled">
      <Textarea v-model="policy" disabled rows="3" />
    </Variant>
  </Story>
</template>
