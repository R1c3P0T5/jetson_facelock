import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Empty from './Empty.vue'

describe('Empty', () => {
  it('renders title', () => {
    const wrapper = mount(Empty, { props: { title: 'No data found' } })
    expect(wrapper.text()).toContain('No data found')
  })

  it('renders description when provided', () => {
    const wrapper = mount(Empty, {
      props: { title: 'Empty', description: 'Try scanning again.' },
    })
    expect(wrapper.text()).toContain('Try scanning again.')
  })

  it('omits description element when not provided', () => {
    const wrapper = mount(Empty, { props: { title: 'Empty' } })
    expect(wrapper.find('[data-empty-description]').exists()).toBe(false)
  })

  it('renders icon slot', () => {
    const wrapper = mount(Empty, {
      props: { title: 'Empty' },
      slots: { icon: '<span data-test="icon">○</span>' },
    })
    expect(wrapper.find('[data-test="icon"]').exists()).toBe(true)
  })

  it('renders default slot for actions', () => {
    const wrapper = mount(Empty, {
      props: { title: 'Empty' },
      slots: { default: '<button data-test="btn">Retry</button>' },
    })
    expect(wrapper.find('[data-test="btn"]').exists()).toBe(true)
  })
})
