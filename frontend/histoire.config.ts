import { defineConfig } from 'histoire'
import { HstVue } from '@histoire/plugin-vue'

export default defineConfig({
  plugins: [HstVue()],
  setupFile: './src/lib/histoire-setup.ts',
  storyMatch: ['src/lib/**/*.story.vue'],
  theme: {
    title: 'Door Lock UI',
  },
})
