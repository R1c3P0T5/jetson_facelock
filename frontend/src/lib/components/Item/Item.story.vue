<script setup lang="ts">
import Badge from '../Badge/Badge.vue'
import Item from './Item.vue'

defineOptions({ name: 'ItemStory' })
</script>

<template>
  <Story title="Layout / Item" :layout="{ type: 'grid', width: 360 }">
    <Variant title="Simple interactive list">
      <div class="rounded-[2px] border border-border bg-subtle p-1.5">
        <Item label="Open in timeline" :interactive="true" />
        <Item label="Mark as reviewed" :interactive="true" />
        <hr class="my-1 border-border-soft" />
        <Item label="Create incident" :interactive="true" />
        <Item label="Download snapshot" :interactive="true" />
      </div>
    </Variant>

    <Variant title="With description">
      <div class="rounded-[2px] border border-border bg-subtle p-1.5">
        <Item label="CAM-01 · Main gate" description="Sampling every 250ms" :interactive="true" />
        <Item label="CAM-02 · Loading bay" description="Sampling every 500ms" :interactive="true" />
        <Item
          label="CAM-03 · Server room"
          description="Offline — last seen 4h ago"
          :interactive="true"
          :disabled="true"
        />
      </div>
    </Variant>

    <Variant title="With trailing badge">
      <div class="rounded-[2px] border border-border bg-subtle p-1.5">
        <Item label="Realtime mode" description="Streaming active" :interactive="true">
          <template #trailing>
            <Badge variant="ok">On</Badge>
          </template>
        </Item>
        <Item label="Auto quarantine" :interactive="true">
          <template #trailing>
            <Badge variant="dim">Off</Badge>
          </template>
        </Item>
      </div>
    </Variant>
  </Story>
</template>
