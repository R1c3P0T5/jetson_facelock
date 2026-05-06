<script setup lang="ts">
import Accordion from './Accordion.vue'
import AccordionItem from './AccordionItem.vue'

defineOptions({ name: 'AccordionStory' })
</script>

<template>
  <Story title="Accordion" :layout="{ type: 'grid', width: 480 }">
    <Variant title="Default (all closed)">
      <Accordion>
        <AccordionItem title="Policy mismatch">
          Collector endpoint timeout. Retry with exponential backoff after 3 attempts.
        </AccordionItem>
        <AccordionItem title="Webhook retries">
          3 retries pending for tenant HK-2 after signature failure.
        </AccordionItem>
        <AccordionItem title="Audit log sync">
          Last sync completed 4 hours ago. Next scheduled at 02:00 UTC.
        </AccordionItem>
      </Accordion>
    </Variant>

    <Variant title="First item open">
      <Accordion>
        <AccordionItem title="Policy mismatch" :open="true">
          Collector endpoint timeout. Retry with exponential backoff after 3 attempts.
        </AccordionItem>
        <AccordionItem title="Webhook retries">
          3 retries pending for tenant HK-2 after signature failure.
        </AccordionItem>
      </Accordion>
    </Variant>
  </Story>
</template>
