import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Switch from './Switch.vue'

describe('Switch', () => {
  it('renders as a button', () => {
    const wrapper = mount(Switch, { props: { modelValue: false } })

    expect(wrapper.find('button').exists()).toBe(true)
  })

  it('emits update:modelValue with toggled value on click', async () => {
    const wrapper = mount(Switch, { props: { modelValue: false } })

    await wrapper.find('button').trigger('click')

    expect(wrapper.emitted('update:modelValue')?.[0]).toEqual([true])
  })

  it('emits false when currently true', async () => {
    const wrapper = mount(Switch, { props: { modelValue: true } })

    await wrapper.find('button').trigger('click')

    expect(wrapper.emitted('update:modelValue')?.[0]).toEqual([false])
  })

  it('shows label when provided', () => {
    const wrapper = mount(Switch, { props: { modelValue: false, label: 'Realtime mode' } })

    expect(wrapper.text()).toBe('Realtime mode')
  })

  it('sets aria-checked based on modelValue', () => {
    const wrapper = mount(Switch, { props: { modelValue: true } })

    expect(wrapper.find('button').attributes('aria-checked')).toBe('true')
  })

  it('uses a squared-off switch style', () => {
    const wrapper = mount(Switch, { props: { modelValue: true } })
    const button = wrapper.find('button')
    const indicator = button.find('span')

    expect(button.classes()).toEqual(expect.arrayContaining(['h-5.5', 'w-10.5', 'rounded-[2px]']))
    expect(button.classes()).not.toContain('rounded-full')
    expect(indicator.classes()).toEqual(
      expect.arrayContaining(['h-3.5', 'w-3.5', 'rounded-[1px]', 'translate-x-5']),
    )
    expect(indicator.classes()).not.toContain('rounded-full')
  })

  it('does not emit when disabled', async () => {
    const wrapper = mount(Switch, { props: { modelValue: false, disabled: true } })

    await wrapper.find('button').trigger('click')

    expect(wrapper.emitted('update:modelValue')).toBeUndefined()
  })
})
