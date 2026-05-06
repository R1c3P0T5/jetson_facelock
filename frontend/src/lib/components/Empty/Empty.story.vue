<script setup lang="ts">
import Button from '../Button/Button.vue'
import Empty from './Empty.vue'

defineOptions({ name: 'EmptyStory' })
</script>

<template>
  <Story title="Feedback / Empty" :layout="{ type: 'grid', width: 480 }">
    <Variant title="With description + action">
      <Empty
        title="No matched record"
        description="Try another sample or refine camera angle before scanning again."
      >
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
          </svg>
        </template>
        <Button variant="secondary" size="sm">Scan again</Button>
      </Empty>
    </Variant>

    <Variant title="No icon">
      <Empty
        title="No critical alerts"
        description="Last severity=high incident closed 2 hours ago."
      />
    </Variant>

    <Variant title="Icon only + title">
      <Empty title="No data yet">
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z" />
          </svg>
        </template>
      </Empty>
    </Variant>
  </Story>
</template>
