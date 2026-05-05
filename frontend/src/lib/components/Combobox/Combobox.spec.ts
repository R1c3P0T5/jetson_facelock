import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Combobox from './Combobox.vue'

const options = [
  { value: 'front-door', label: 'Front door' },
  { value: 'garage', label: 'Garage' },
  { value: 'server-room', label: 'Server room', disabled: true },
]

describe('Combobox', () => {
  it('shows the selected option label', () => {
    const wrapper = mount(Combobox, { props: { modelValue: 'garage', options } })

    expect((wrapper.find('input').element as HTMLInputElement).value).toBe('Garage')
  })

  it('opens and filters options by typed text', async () => {
    const wrapper = mount(Combobox, { props: { modelValue: '', options } })

    await wrapper.find('input').trigger('focus')
    await wrapper.find('input').setValue('front')

    expect(wrapper.find('[role="listbox"]').exists()).toBe(true)
    expect(wrapper.findAll('[role="option"]')).toHaveLength(1)
    expect(wrapper.text()).toContain('Front door')
  })

  it('emits update:modelValue and closes when an enabled option is selected', async () => {
    const wrapper = mount(Combobox, { props: { modelValue: '', options } })

    await wrapper.find('input').trigger('focus')
    await wrapper.find('button[data-value="garage"]').trigger('click')

    expect(wrapper.emitted('update:modelValue')?.[0]).toEqual(['garage'])
    expect(wrapper.find('[role="listbox"]').exists()).toBe(false)
  })

  it('does not emit for disabled options', async () => {
    const wrapper = mount(Combobox, { props: { modelValue: '', options } })

    await wrapper.find('input').trigger('focus')
    await wrapper.find('button[data-value="server-room"]').trigger('click')

    expect(wrapper.emitted('update:modelValue')).toBeUndefined()
  })

  it('does not open while disabled', async () => {
    const wrapper = mount(Combobox, { props: { modelValue: '', options, disabled: true } })

    await wrapper.find('input').trigger('focus')

    expect(wrapper.find('[role="listbox"]').exists()).toBe(false)
  })

  it('applies invalid state from prop or aria-invalid attr', () => {
    const propWrapper = mount(Combobox, { props: { modelValue: '', options, invalid: true } })
    const attrWrapper = mount(Combobox, {
      props: { modelValue: '', options },
      attrs: { 'aria-invalid': 'true' },
    })

    expect(propWrapper.find('input').classes()).toContain('border-err')
    expect(propWrapper.find('input').attributes('aria-invalid')).toBe('true')
    expect(attrWrapper.find('input').classes()).toContain('border-err')
  })
})
