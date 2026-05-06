<script setup lang="ts">
defineOptions({ name: 'UiBreadcrumb' })

export interface BreadcrumbItem {
  label: string
  href?: string
}

const props = defineProps<{
  items: BreadcrumbItem[]
}>()
</script>

<template>
  <nav aria-label="Breadcrumb">
    <ol class="flex flex-wrap items-center gap-2 font-mono text-[11px] uppercase tracking-[0.06em]">
      <li v-for="(item, i) in props.items" :key="i" class="flex items-center gap-2">
        <span v-if="i > 0" aria-hidden="true" class="text-text-placeholder">/</span>
        <component
          :is="item.href ? 'a' : 'span'"
          :href="item.href"
          :aria-current="i === props.items.length - 1 ? 'page' : undefined"
          :class="[
            i === props.items.length - 1
              ? 'text-text-hi'
              : 'text-text-placeholder hover:text-text-lo transition-colors',
            item.href && 'no-underline',
          ]"
        >
          {{ item.label }}
        </component>
      </li>
    </ol>
  </nav>
</template>
