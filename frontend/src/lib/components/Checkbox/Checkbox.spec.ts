import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Checkbox from './Checkbox.vue'

describe('Checkbox', () => {
  it('renders a native checkbox input', () => {
    const wrapper = mount(Checkbox, { props: { modelValue: false } })
    const input = wrapper.find('input[type="checkbox"]')

    expect(input.exists()).toBe(true)
    expect((input.element as HTMLInputElement).checked).toBe(false)
  })

  it('emits update:modelValue with the toggled value', async () => {
    const wrapper = mount(Checkbox, { props: { modelValue: false } })

    await wrapper.find('input').setValue(true)

    expect(wrapper.emitted('update:modelValue')?.[0]).toEqual([true])
  })

  it('shows checked state', () => {
    const wrapper = mount(Checkbox, { props: { modelValue: true } })

    expect((wrapper.find('input').element as HTMLInputElement).checked).toBe(true)
  })

  it('does not emit while disabled', async () => {
    const wrapper = mount(Checkbox, { props: { modelValue: false, disabled: true } })

    await wrapper.find('input').trigger('change')

    expect(wrapper.emitted('update:modelValue')).toBeUndefined()
  })

  it('applies invalid state from prop or aria-invalid attr', () => {
    const propWrapper = mount(Checkbox, { props: { modelValue: false, invalid: true } })
    const attrWrapper = mount(Checkbox, {
      props: { modelValue: false },
      attrs: { 'aria-invalid': 'true' },
    })

    expect(propWrapper.find('input').classes()).toContain('outline-err')
    expect(propWrapper.find('input').attributes('aria-invalid')).toBe('true')
    expect(attrWrapper.find('input').classes()).toContain('outline-err')
  })

  it('renders label and description when provided', () => {
    const wrapper = mount(Checkbox, {
      props: {
        modelValue: false,
        label: 'Accept terms',
        description: 'You agree to the terms.',
      },
    })

    expect(wrapper.text()).toContain('Accept terms')
    expect(wrapper.text()).toContain('You agree to the terms.')
  })
})
