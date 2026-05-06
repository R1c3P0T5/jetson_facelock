import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Progress from './Progress.vue'

describe('Progress', () => {
  it('sets width to percentage of value/max', () => {
    const wrapper = mount(Progress, { props: { value: 50 } })
    const bar = wrapper.find('[data-progress-bar]')
    expect(bar.attributes('style')).toContain('width: 50%')
  })

  it('clamps value above max to 100%', () => {
    const wrapper = mount(Progress, { props: { value: 150 } })
    const bar = wrapper.find('[data-progress-bar]')
    expect(bar.attributes('style')).toContain('width: 100%')
  })

  it('clamps negative value to 0%', () => {
    const wrapper = mount(Progress, { props: { value: -10 } })
    const bar = wrapper.find('[data-progress-bar]')
    expect(bar.attributes('style')).toContain('width: 0%')
  })

  it('respects custom max', () => {
    const wrapper = mount(Progress, { props: { value: 3, max: 4 } })
    const bar = wrapper.find('[data-progress-bar]')
    expect(bar.attributes('style')).toContain('width: 75%')
  })

  it('has progressbar aria role', () => {
    const wrapper = mount(Progress, { props: { value: 50 } })
    expect(wrapper.attributes('role')).toBe('progressbar')
  })
})
