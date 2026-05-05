import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Tabs from './Tabs.vue'

const tabs = [
  { key: 'live', label: 'Live logs' },
  { key: 'alerts', label: 'Alerts' },
  { key: 'audit', label: 'Audit' },
]

describe('Tabs', () => {
  it('renders all tab buttons', () => {
    const wrapper = mount(Tabs, { props: { tabs, modelValue: 'live' } })
    const buttons = wrapper.findAll('[role="tab"]')
    expect(buttons).toHaveLength(3)
    expect(buttons[0]!.text()).toBe('Live logs')
  })

  it('marks active tab with aria-selected="true"', () => {
    const wrapper = mount(Tabs, { props: { tabs, modelValue: 'alerts' } })
    const alertsTab = wrapper.findAll('[role="tab"]')[1]!
    expect(alertsTab.attributes('aria-selected')).toBe('true')
  })

  it('emits update:modelValue with tab key on click', async () => {
    const wrapper = mount(Tabs, { props: { tabs, modelValue: 'live' } })
    await wrapper.findAll('[role="tab"]')[2]!.trigger('click')
    expect(wrapper.emitted('update:modelValue')?.[0]).toEqual(['audit'])
  })
})
