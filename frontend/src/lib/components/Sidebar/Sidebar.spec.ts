import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Sidebar from './Sidebar.vue'

describe('Sidebar', () => {
  it('renders brand title', () => {
    const wrapper = mount(Sidebar, { props: { brand: 'FaceGuard' } })
    expect(wrapper.text()).toContain('FaceGuard')
  })

  it('renders default slot as nav area', () => {
    const wrapper = mount(Sidebar, {
      props: { brand: 'App' },
      slots: { default: '<div data-test="nav">nav</div>' },
    })
    expect(wrapper.find('[data-test="nav"]').exists()).toBe(true)
  })

  it('renders header slot below brand', () => {
    const wrapper = mount(Sidebar, {
      props: { brand: 'App' },
      slots: { header: '<p data-test="header">meta</p>' },
    })
    expect(wrapper.find('[data-test="header"]').exists()).toBe(true)
  })

  it('renders footer slot at bottom', () => {
    const wrapper = mount(Sidebar, {
      props: { brand: 'App' },
      slots: { footer: '<p data-test="footer">v1.0</p>' },
    })
    expect(wrapper.find('[data-test="footer"]').exists()).toBe(true)
  })

  it('renders brand-action slot beside brand title', () => {
    const wrapper = mount(Sidebar, {
      props: { brand: 'App' },
      slots: { 'brand-action': '<span data-test="badge">v2</span>' },
    })
    expect(wrapper.find('[data-test="badge"]').exists()).toBe(true)
  })
})
