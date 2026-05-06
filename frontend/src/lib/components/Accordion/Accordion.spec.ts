import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Accordion from './Accordion.vue'
import AccordionItem from './AccordionItem.vue'

describe('AccordionItem', () => {
  it('renders title', () => {
    const wrapper = mount(AccordionItem, {
      props: { title: 'Policy mismatch' },
      slots: { default: 'Content here' },
    })
    expect(wrapper.text()).toContain('Policy mismatch')
  })

  it('hides panel content by default', () => {
    const wrapper = mount(AccordionItem, {
      props: { title: 'Item' },
      slots: { default: '<p data-test="content">Body</p>' },
    })
    const panel = wrapper.find('[data-accordion-panel]')
    expect(panel.isVisible()).toBe(false)
  })

  it('shows panel when open prop is true', () => {
    const wrapper = mount(AccordionItem, {
      props: { title: 'Item', open: true },
      slots: { default: '<p data-test="content">Body</p>' },
    })
    const panel = wrapper.find('[data-accordion-panel]')
    expect(panel.isVisible()).toBe(true)
  })

  it('toggles open on button click', async () => {
    const wrapper = mount(AccordionItem, {
      props: { title: 'Item' },
      slots: { default: 'Content' },
    })
    await wrapper.find('button').trigger('click')
    expect(wrapper.find('[data-accordion-panel]').isVisible()).toBe(true)
  })

  it('emits update:open on toggle', async () => {
    const wrapper = mount(AccordionItem, {
      props: { title: 'Item', open: false },
      slots: { default: 'Content' },
    })
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted('update:open')?.[0]).toEqual([true])
  })
})

describe('Accordion', () => {
  it('renders slotted AccordionItems', () => {
    const wrapper = mount(Accordion, {
      slots: {
        default: '<div data-test="item1">A</div><div data-test="item2">B</div>',
      },
    })
    expect(wrapper.find('[data-test="item1"]').exists()).toBe(true)
    expect(wrapper.find('[data-test="item2"]').exists()).toBe(true)
  })
})
