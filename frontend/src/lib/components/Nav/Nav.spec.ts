import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Nav from './Nav.vue'
import NavItem from './NavItem.vue'

const items = [
  { key: 'overview', label: 'Overview', href: '#overview' },
  { key: 'primitives', label: 'Primitives', href: '#primitives' },
  { key: 'forms', label: 'Form controls', href: '#forms' },
]

describe('Nav', () => {
  it('renders slotted content', () => {
    const wrapper = mount(Nav, { slots: { default: '<div data-test="inner">x</div>' } })
    expect(wrapper.find('[data-test="inner"]').exists()).toBe(true)
  })
})

describe('NavItem', () => {
  it('renders label', () => {
    const wrapper = mount(NavItem, { props: { label: 'Overview', href: '#overview' } })
    expect(wrapper.text()).toContain('Overview')
  })

  it('renders as anchor with href', () => {
    const wrapper = mount(NavItem, { props: { label: 'Overview', href: '#overview' } })
    expect(wrapper.find('a').attributes('href')).toBe('#overview')
  })

  it('applies active styles when active prop is true', () => {
    const wrapper = mount(NavItem, {
      props: { label: 'Active', href: '#active', active: true },
    })
    expect(wrapper.classes().some((c) => c.includes('border-border'))).toBe(true)
  })

  it('emits click when clicked', async () => {
    const wrapper = mount(NavItem, { props: { label: 'Nav', href: '#nav' } })
    await wrapper.find('a').trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })
})

describe('Nav with items prop', () => {
  it('renders all items', () => {
    const wrapper = mount(Nav, { props: { items } })
    expect(wrapper.text()).toContain('Overview')
    expect(wrapper.text()).toContain('Primitives')
    expect(wrapper.text()).toContain('Form controls')
  })

  it('marks active item', () => {
    const wrapper = mount(Nav, { props: { items, modelValue: 'primitives' } })
    const links = wrapper.findAll('a')
    const primitives = links.find((l) => l.text().includes('Primitives'))
    expect(primitives?.classes().some((c) => c.includes('text-text-hi'))).toBe(true)
  })
})
