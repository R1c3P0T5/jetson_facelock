import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import RadioGroup from './RadioGroup.vue'

const options = [
  { value: 'pin', label: 'PIN' },
  { value: 'face', label: 'Face unlock', description: 'Use camera verification.' },
  { value: 'card', label: 'Access card', disabled: true },
]

describe('RadioGroup', () => {
  it('renders one radio for each option', () => {
    const wrapper = mount(RadioGroup, { props: { modelValue: 'pin', options } })

    expect(wrapper.findAll('input[type="radio"]')).toHaveLength(3)
    expect(wrapper.text()).toContain('Face unlock')
    expect(wrapper.text()).toContain('Use camera verification.')
  })

  it('checks the option matching modelValue', () => {
    const wrapper = mount(RadioGroup, { props: { modelValue: 'face', options } })

    expect((wrapper.find('input[value="face"]').element as HTMLInputElement).checked).toBe(true)
  })

  it('emits update:modelValue when an enabled option is selected', async () => {
    const wrapper = mount(RadioGroup, { props: { modelValue: 'pin', options } })

    await wrapper.find('input[value="face"]').setValue(true)

    expect(wrapper.emitted('update:modelValue')?.[0]).toEqual(['face'])
  })

  it('does not emit for disabled options', async () => {
    const wrapper = mount(RadioGroup, { props: { modelValue: 'pin', options } })

    await wrapper.find('input[value="card"]').trigger('change')

    expect(wrapper.emitted('update:modelValue')).toBeUndefined()
  })

  it('applies invalid state to the group and radios', () => {
    const wrapper = mount(RadioGroup, { props: { modelValue: 'pin', options, invalid: true } })

    expect(wrapper.attributes('aria-invalid')).toBe('true')
    expect(wrapper.find('input').classes()).toContain('outline-err')
  })
})
