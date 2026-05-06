import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Item from './Item.vue'

describe('Item', () => {
  it('renders label', () => {
    const wrapper = mount(Item, { props: { label: 'Open in timeline' } })
    expect(wrapper.text()).toContain('Open in timeline')
  })

  it('renders description when provided', () => {
    const wrapper = mount(Item, {
      props: { label: 'Camera source', description: 'CAM-01 · Main gate' },
    })
    expect(wrapper.text()).toContain('CAM-01 · Main gate')
  })

  it('omits description element when not provided', () => {
    const wrapper = mount(Item, { props: { label: 'Label only' } })
    expect(wrapper.find('[data-item-description]').exists()).toBe(false)
  })

  it('renders icon slot', () => {
    const wrapper = mount(Item, {
      props: { label: 'Item' },
      slots: { icon: '<span data-test="icon">●</span>' },
    })
    expect(wrapper.find('[data-test="icon"]').exists()).toBe(true)
  })

  it('renders trailing slot', () => {
    const wrapper = mount(Item, {
      props: { label: 'Item' },
      slots: { trailing: '<kbd data-test="kbd">⌘K</kbd>' },
    })
    expect(wrapper.find('[data-test="kbd"]').exists()).toBe(true)
  })

  it('applies disabled state', () => {
    const wrapper = mount(Item, { props: { label: 'Disabled', disabled: true } })
    expect(wrapper.classes().some((c) => c.includes('opacity-50'))).toBe(true)
  })

  it('emits click when interactive and not disabled', async () => {
    const wrapper = mount(Item, { props: { label: 'Click me', interactive: true } })
    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })
})
