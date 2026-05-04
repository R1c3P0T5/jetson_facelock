import { defineConfig } from 'histoire'
import { HstVue } from '@histoire/plugin-vue'

export default defineConfig({
  plugins: [HstVue()],
  setupFile: './src/lib/histoire-setup.ts',
  storyMatch: ['src/lib/**/*.story.vue'],
  theme: {
    title: 'Door Lock UI',
  },
  tree: {
    groups: [
      { title: 'Primitives', include: f => ['Button', 'Badge', 'Alert'].some(n => f.title.includes(n)) },
      { title: 'Form', include: f => ['Input', 'Switch'].some(n => f.title.includes(n)) },
      { title: 'Navigation', include: f => f.title.includes('Tabs') },
      { title: 'Overlay', include: f => ['Toast', 'Dialog'].some(n => f.title.includes(n)) },
    ],
  },
})
