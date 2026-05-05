<script setup lang="ts">
import Button from '../Button/Button.vue'
import Toast from './Toast.vue'
import { useToast } from './useToast'

defineOptions({ name: 'ToastStory' })

const { show } = useToast()
</script>

<template>
  <Story title="Toast" :layout="{ type: 'single', iframe: false }">
    <Variant title="Trigger">
      <Toast />
      <div class="flex gap-2">
        <Button
          variant="secondary"
          @click="show({ title: 'Settings saved', message: 'Theme applied.' })"
        >
          Show toast
        </Button>
        <Button variant="secondary" @click="show({ title: 'Sync complete' })">
          Show minimal
        </Button>
      </div>
    </Variant>
  </Story>
</template>
