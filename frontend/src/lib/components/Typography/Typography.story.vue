<script setup lang="ts">
defineOptions({ name: 'TypographyStory' })
</script>

<template>
  <Story title="Typography" :layout="{ type: 'single', iframe: false }">
    <Variant title="Type scale">
      <div class="grid gap-6 p-4">
        <!-- Headings -->
        <section class="grid gap-3">
          <p class="font-mono text-[11px] uppercase tracking-[0.1em] text-text-placeholder">
            Headings — font-mono uppercase
          </p>
          <div class="grid gap-2">
            <h1 class="font-mono text-2xl uppercase tracking-[0.04em] text-text-hi">
              H1 · FaceGuard Node Security
            </h1>
            <h2 class="font-mono text-xl uppercase tracking-[0.04em] text-text-hi">
              H2 · Access control policy
            </h2>
            <h3 class="font-mono text-base uppercase tracking-[0.05em] text-text-hi">
              H3 · Camera source settings
            </h3>
            <h4 class="font-mono text-sm uppercase tracking-[0.05em] text-text-hi">
              H4 · Latency threshold
            </h4>
          </div>
        </section>

        <hr class="border-border-soft" />

        <!-- Kicker / label -->
        <section class="grid gap-3">
          <p class="font-mono text-[11px] uppercase tracking-[0.1em] text-text-placeholder">
            Kicker — mono 11px 0.1em
          </p>
          <div class="grid gap-2">
            <p class="font-mono text-[11px] uppercase tracking-[0.1em] text-text-placeholder">
              Section label · sub-category
            </p>
            <p class="font-mono text-[11px] uppercase tracking-[0.08em] text-text-placeholder">
              Form label · employee id
            </p>
          </div>
        </section>

        <hr class="border-border-soft" />

        <!-- Body -->
        <section class="grid gap-3">
          <p class="font-mono text-[11px] uppercase tracking-[0.1em] text-text-placeholder">
            Body — font-sans
          </p>
          <div class="grid gap-2">
            <p class="text-base text-text-hi">
              Base (16px) · 保留原始 FaceGuard 的深色 utility
              語彙，同時把元件尺寸提升到更可讀的工程展示尺度。
            </p>
            <p class="text-sm text-text-hi">
              Small (14px) · Collector endpoint timeout. Retry with exponential backoff after 3
              attempts.
            </p>
            <p class="text-xs text-text-lo">
              XS (12px) · Sampling every 250ms · Edge runtime · p95 latency
            </p>
          </div>
        </section>

        <hr class="border-border-soft" />

        <!-- Color hierarchy -->
        <section class="grid gap-3">
          <p class="font-mono text-[11px] uppercase tracking-[0.1em] text-text-placeholder">
            Color hierarchy
          </p>
          <div class="grid gap-1.5">
            <p class="text-sm text-text-hi">text-hi · Primary content, headings, values</p>
            <p class="text-sm text-text-lo">text-lo · Secondary content, descriptions</p>
            <p class="text-sm text-text-placeholder">text-placeholder · Labels, hints, metadata</p>
            <p class="text-sm text-ok">text-ok · Success, granted, healthy</p>
            <p class="text-sm text-warn">text-warn · Warning, review, elevated</p>
            <p class="text-sm text-err">text-err · Error, denied, failed</p>
            <p class="text-sm text-ac">text-ac · Accent, interactive, focus</p>
          </div>
        </section>

        <hr class="border-border-soft" />

        <!-- Mono specimens -->
        <section class="grid gap-3">
          <p class="font-mono text-[11px] uppercase tracking-[0.1em] text-text-placeholder">
            Monospace — tabular numerics
          </p>
          <div class="grid gap-1.5">
            <p class="font-mono text-sm tabular-nums text-text-hi">
              14:41:18 · CAM-01 · 98.4% · 11ms
            </p>
            <p class="font-mono text-xs tabular-nums text-text-lo">
              FG-0138 · edge-node-07 · policy-v2
            </p>
            <p class="font-mono text-2xl tabular-nums tracking-[0.02em] text-text-hi">1,284</p>
          </div>
        </section>
      </div>
    </Variant>
  </Story>
</template>
