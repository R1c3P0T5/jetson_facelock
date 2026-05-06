import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Breadcrumb from './Breadcrumb.vue'

const items = [{ label: 'ops' }, { label: 'access-control', href: '/access' }, { label: 'policy' }]

describe('Breadcrumb', () => {
  it('renders all item labels', () => {
    const wrapper = mount(Breadcrumb, { props: { items } })
    expect(wrapper.text()).toContain('ops')
    expect(wrapper.text()).toContain('access-control')
    expect(wrapper.text()).toContain('policy')
  })

  it('renders href items as anchor tags', () => {
    const wrapper = mount(Breadcrumb, { props: { items } })
    const links = wrapper.findAll('a')
    expect(links).toHaveLength(1)
    expect(links[0]!.attributes('href')).toBe('/access')
  })

  it('marks last item as active', () => {
    const wrapper = mount(Breadcrumb, { props: { items } })
    const active = wrapper.find('[aria-current="page"]')
    expect(active.text()).toBe('policy')
  })

  it('renders separator between items', () => {
    const wrapper = mount(Breadcrumb, { props: { items } })
    expect(wrapper.findAll('[aria-hidden="true"]')).toHaveLength(items.length - 1)
  })
})
