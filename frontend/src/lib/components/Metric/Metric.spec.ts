import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Metric from './Metric.vue'

describe('Metric', () => {
  it('renders label and value', () => {
    const wrapper = mount(Metric, { props: { label: 'Today scans', value: '1,284' } })
    expect(wrapper.text()).toContain('Today scans')
    expect(wrapper.text()).toContain('1,284')
  })

  it('renders delta when provided', () => {
    const wrapper = mount(Metric, {
      props: { label: 'Grant rate', value: '97.2%', delta: '+3.1%' },
    })
    expect(wrapper.text()).toContain('+3.1%')
  })

  it('omits delta element when not provided', () => {
    const wrapper = mount(Metric, { props: { label: 'Latency', value: '12ms' } })
    expect(wrapper.find('[data-metric-delta]').exists()).toBe(false)
  })
})
