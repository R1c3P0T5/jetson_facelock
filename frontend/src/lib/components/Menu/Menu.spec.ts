import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Menu from './Menu.vue'
import MenuItem from './MenuItem.vue'
import MenuSeparator from './MenuSeparator.vue'

describe('Menu', () => {
  it('renders slotted content', () => {
    const wrapper = mount(Menu, { slots: { default: '<div data-test="inner">x</div>' } })
    expect(wrapper.find('[data-test="inner"]').exists()).toBe(true)
  })
})

describe('MenuItem', () => {
  it('renders label', () => {
    const wrapper = mount(MenuItem, { props: { label: 'Open timeline' } })
    expect(wrapper.text()).toContain('Open timeline')
  })

  it('emits click on interaction', async () => {
    const wrapper = mount(MenuItem, { props: { label: 'Action' } })
    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })

  it('does not emit click when disabled', async () => {
    const wrapper = mount(MenuItem, { props: { label: 'Disabled', disabled: true } })
    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toBeFalsy()
  })

  it('applies destructive style', () => {
    const wrapper = mount(MenuItem, { props: { label: 'Delete', destructive: true } })
    expect(wrapper.classes().some((c) => c.includes('text-err'))).toBe(true)
  })
})

describe('MenuSeparator', () => {
  it('renders an hr element', () => {
    const wrapper = mount(MenuSeparator)
    expect(wrapper.element.tagName.toLowerCase()).toBe('hr')
  })
})
