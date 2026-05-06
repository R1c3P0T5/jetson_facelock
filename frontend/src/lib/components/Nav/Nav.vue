<script setup lang="ts">
defineOptions({ name: 'UiNav' })

export interface NavItemDef {
  key: string
  label: string
  href?: string
}

withDefaults(
  defineProps<{
    items?: NavItemDef[]
    modelValue?: string
  }>(),
  {
    items: undefined,
    modelValue: undefined,
  },
)

const emit = defineEmits<{
  'update:modelValue': [key: string]
  click: [item: NavItemDef]
}>()
</script>

<template>
  <nav aria-label="Navigation" class="grid gap-1">
    <template v-if="items">
      <a
        v-for="item in items"
        :key="item.key"
        :href="item.href"
        :aria-current="modelValue === item.key ? 'page' : undefined"
        :class="[
          'grid cursor-pointer grid-cols-[6px_1fr] items-center gap-2.5 rounded-[2px] border px-2.5 py-2.5 font-mono text-[11px] uppercase tracking-[0.07em] no-underline transition-colors duration-[120ms]',
          'focus-visible:outline focus-visible:outline-1 focus-visible:outline-ac focus-visible:outline-offset-2',
          modelValue === item.key
            ? 'border-border bg-element text-text-hi'
            : 'border-transparent text-text-lo hover:border-border hover:bg-overlay hover:text-text-hi',
        ]"
        @click.prevent="
          emit('update:modelValue', item.key)
          emit('click', item)
        "
      >
        <span
          :class="['h-1.5 w-1.5 rounded-full', modelValue === item.key ? 'bg-ac' : 'bg-border']"
          aria-hidden="true"
        />
        {{ item.label }}
      </a>
    </template>
    <slot v-else />
  </nav>
</template>
