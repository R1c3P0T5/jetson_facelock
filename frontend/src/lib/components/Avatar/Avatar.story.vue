<script setup lang="ts">
import Avatar from './Avatar.vue'
import AvatarStack from './AvatarStack.vue'

defineOptions({ name: 'AvatarStory' })
</script>

<template>
  <Story title="Data / Avatar" :layout="{ type: 'grid', width: 320 }">
    <Variant title="Sizes">
      <div class="flex items-end gap-3">
        <Avatar initials="SM" size="sm" />
        <Avatar initials="MD" size="md" />
        <Avatar initials="LG" size="lg" />
      </div>
    </Variant>

    <Variant title="Stack">
      <AvatarStack>
        <Avatar initials="LW" />
        <Avatar initials="YC" />
        <Avatar initials="JM" />
        <Avatar initials="+2" />
      </AvatarStack>
    </Variant>
  </Story>
</template>
