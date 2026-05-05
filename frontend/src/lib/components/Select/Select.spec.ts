import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Select from './Select.vue'

const options = [
  { value: 'always', label: 'Always allow' },
  { value: 'approval', label: 'Require approval' },
  { value: 'offline', label: 'Offline only', disabled: true },
]

describe('Select', () => {
  it('shows placeholder when no value is selected', () => {
    const wrapper = mount(Select, {
      props: { modelValue: '', options, placeholder: 'Choose mode' },
    })

    expect(wrapper.find('button[aria-haspopup="listbox"]').text()).toContain('Choose mode')
  })

  it('shows the label for modelValue', () => {
    const wrapper = mount(Select, { props: { modelValue: 'approval', options } })

    expect(wrapper.find('button[aria-haspopup="listbox"]').text()).toContain('Require approval')
  })

  it('opens and closes the option list from the trigger', async () => {
    const wrapper = mount(Select, { props: { modelValue: '', options } })
    const trigger = wrapper.find('button[aria-haspopup="listbox"]')

    await trigger.trigger('click')
    expect(wrapper.find('[role="listbox"]').exists()).toBe(true)
    expect(trigger.attributes('aria-expanded')).toBe('true')

    await trigger.trigger('click')
    expect(wrapper.find('[role="listbox"]').exists()).toBe(false)
  })

  it('emits update:modelValue and closes when an enabled option is selected', async () => {
    const wrapper = mount(Select, { props: { modelValue: '', options } })

    await wrapper.find('button[aria-haspopup="listbox"]').trigger('click')
    await wrapper.find('button[data-value="approval"]').trigger('click')

    expect(wrapper.emitted('update:modelValue')?.[0]).toEqual(['approval'])
    expect(wrapper.find('[role="listbox"]').exists()).toBe(false)
  })

  it('does not emit for disabled options', async () => {
    const wrapper = mount(Select, { props: { modelValue: '', options } })

    await wrapper.find('button[aria-haspopup="listbox"]').trigger('click')
    await wrapper.find('button[data-value="offline"]').trigger('click')

    expect(wrapper.emitted('update:modelValue')).toBeUndefined()
  })

  it('applies invalid state from prop or aria-invalid attr', () => {
    const propWrapper = mount(Select, { props: { modelValue: '', options, invalid: true } })
    const attrWrapper = mount(Select, {
      props: { modelValue: '', options },
      attrs: { 'aria-invalid': 'true' },
    })

    expect(propWrapper.find('button[aria-haspopup="listbox"]').classes()).toContain('border-err')
    expect(propWrapper.find('button[aria-haspopup="listbox"]').attributes('aria-invalid')).toBe(
      'true',
    )
    expect(attrWrapper.find('button[aria-haspopup="listbox"]').classes()).toContain('border-err')
  })
})
