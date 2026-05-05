import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import NativeSelect from './NativeSelect.vue'

const options = [
  { value: 'owner', label: 'Owner' },
  { value: 'guest', label: 'Guest' },
  { value: 'locked', label: 'Locked', disabled: true },
]

describe('NativeSelect', () => {
  it('renders options and the selected value', () => {
    const wrapper = mount(NativeSelect, { props: { modelValue: 'guest', options } })

    expect(wrapper.findAll('option')).toHaveLength(3)
    expect((wrapper.find('select').element as HTMLSelectElement).value).toBe('guest')
  })

  it('renders a disabled placeholder option', () => {
    const wrapper = mount(NativeSelect, {
      props: { modelValue: '', options, placeholder: 'Choose role' },
    })
    const placeholder = wrapper.find('option')

    expect(placeholder.text()).toBe('Choose role')
    expect(placeholder.attributes('disabled')).toBeDefined()
  })

  it('emits update:modelValue when selection changes', async () => {
    const wrapper = mount(NativeSelect, { props: { modelValue: 'owner', options } })

    await wrapper.find('select').setValue('guest')

    expect(wrapper.emitted('update:modelValue')?.[0]).toEqual(['guest'])
  })

  it('marks disabled options', () => {
    const wrapper = mount(NativeSelect, { props: { modelValue: 'owner', options } })

    expect(wrapper.find('option[value="locked"]').attributes('disabled')).toBeDefined()
  })

  it('applies invalid state from prop or aria-invalid attr', () => {
    const propWrapper = mount(NativeSelect, { props: { modelValue: '', options, invalid: true } })
    const attrWrapper = mount(NativeSelect, {
      props: { modelValue: '', options },
      attrs: { 'aria-invalid': 'true' },
    })

    expect(propWrapper.find('select').classes()).toContain('border-err')
    expect(propWrapper.find('select').attributes('aria-invalid')).toBe('true')
    expect(attrWrapper.find('select').classes()).toContain('border-err')
  })
})
