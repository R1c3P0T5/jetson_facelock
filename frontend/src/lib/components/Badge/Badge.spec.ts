import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Badge from './Badge.vue'

describe('Badge', () => {
  it('renders slot content', () => {
    const wrapper = mount(Badge, { slots: { default: 'Granted' } })
    expect(wrapper.text()).toBe('Granted')
  })

  it('applies ok variant classes', () => {
    const wrapper = mount(Badge, { props: { variant: 'ok' } })
    expect(wrapper.classes()).toContain('text-ok')
    expect(wrapper.classes()).toContain('border-ok/50')
  })

  it('applies err variant classes', () => {
    const wrapper = mount(Badge, { props: { variant: 'err' } })
    expect(wrapper.classes()).toContain('text-err')
  })

  it('applies warn variant classes', () => {
    const wrapper = mount(Badge, { props: { variant: 'warn' } })
    expect(wrapper.classes()).toContain('text-warn')
  })

  it('applies dim variant classes by default', () => {
    const wrapper = mount(Badge)
    expect(wrapper.classes()).toContain('text-text-lo')
  })
})
