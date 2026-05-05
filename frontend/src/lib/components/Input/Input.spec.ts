import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Input from './Input.vue'

describe('Input', () => {
  it('renders an input element', () => {
    const wrapper = mount(Input, { props: { modelValue: '' } })

    expect(wrapper.find('input').exists()).toBe(true)
  })

  it('emits update:modelValue on input', async () => {
    const wrapper = mount(Input, { props: { modelValue: '' } })

    await wrapper.find('input').setValue('hello')

    expect(wrapper.emitted('update:modelValue')?.[0]).toEqual(['hello'])
  })

  it('forwards native attributes to the input element', () => {
    const wrapper = mount(Input, {
      props: { modelValue: '' },
      attrs: { placeholder: 'Device ID', type: 'search', name: 'device', class: 'max-w-sm' },
    })
    const input = wrapper.find('input')

    expect(input.attributes('placeholder')).toBe('Device ID')
    expect(input.attributes('type')).toBe('search')
    expect(input.attributes('name')).toBe('device')
    expect(input.classes()).toContain('max-w-sm')
  })

  it('shows prefix text when provided', () => {
    const wrapper = mount(Input, { props: { modelValue: '', prefix: '#' } })

    expect(wrapper.find('[data-prefix]').text()).toBe('#')
  })

  it('shows suffix text when provided', () => {
    const wrapper = mount(Input, { props: { modelValue: '', suffix: '%' } })

    expect(wrapper.find('[data-suffix]').text()).toBe('%')
  })

  it('applies invalid border class when invalid', () => {
    const wrapper = mount(Input, { props: { modelValue: '', invalid: true } })

    expect(wrapper.find('input').classes()).toContain('border-err')
    expect(wrapper.find('input').attributes('aria-invalid')).toBe('true')
  })

  it('supports aria-invalid without the invalid prop', () => {
    const wrapper = mount(Input, { props: { modelValue: '' }, attrs: { 'aria-invalid': 'true' } })

    expect(wrapper.find('input').classes()).toContain('border-err')
  })

  it('styles disabled inputs', () => {
    const wrapper = mount(Input, { props: { modelValue: '' }, attrs: { disabled: true } })

    expect(wrapper.find('input').classes()).toContain('disabled:cursor-not-allowed')
  })

  it('supports file inputs', () => {
    const wrapper = mount(Input, { props: { modelValue: '' }, attrs: { type: 'file' } })

    expect(wrapper.find('input').attributes('type')).toBe('file')
    expect(wrapper.find('input').classes()).toContain('file:border-0')
  })

  it('renders hint text', () => {
    const wrapper = mount(Input, { props: { modelValue: '', hint: 'Must be 8 chars' } })

    expect(wrapper.text()).toContain('Must be 8 chars')
  })

  it('renders error text when invalid', () => {
    const wrapper = mount(Input, { props: { modelValue: '', invalid: true, error: 'Required' } })

    expect(wrapper.text()).toContain('Required')
  })
})
