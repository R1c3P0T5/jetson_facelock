import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Card from './Card.vue'

describe('Card', () => {
  it('renders default slot content', () => {
    const wrapper = mount(Card, { slots: { default: '<p>body</p>' } })
    expect(wrapper.text()).toContain('body')
  })

  it('hides header when no kicker/title/action provided', () => {
    const wrapper = mount(Card, { slots: { default: 'content' } })
    expect(wrapper.find('[data-card-header]').exists()).toBe(false)
  })

  it('shows header when kicker is provided', () => {
    const wrapper = mount(Card, { props: { kicker: 'Data display' } })
    expect(wrapper.find('[data-card-header]').exists()).toBe(true)
    expect(wrapper.text()).toContain('Data display')
  })

  it('shows header when title is provided', () => {
    const wrapper = mount(Card, { props: { title: 'Access log' } })
    expect(wrapper.text()).toContain('Access log')
  })

  it('renders action slot in header', () => {
    const wrapper = mount(Card, {
      props: { title: 'Test' },
      slots: { action: '<span data-test="act">Go</span>' },
    })
    expect(wrapper.find('[data-test="act"]').exists()).toBe(true)
  })
})
