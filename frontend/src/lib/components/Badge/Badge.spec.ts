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

  it('applies info variant classes', () => {
    const wrapper = mount(Badge, { props: { variant: 'info' } })
    expect(wrapper.classes()).toContain('text-info')
    expect(wrapper.classes()).toContain('border-info/50')
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

  it('does not render status dot by default', () => {
    const wrapper = mount(Badge)
    expect(wrapper.find('[aria-hidden="true"]').exists()).toBe(false)
  })

  it('applies custom color styles from a color string', () => {
    const wrapper = mount(Badge, { props: { color: '#326f91' } })

    expect(wrapper.attributes('style')).toContain('--badge-text: #326f91')
    expect(wrapper.classes()).toContain('text-[var(--badge-text)]')
  })

  it('applies custom color styles from color parts', () => {
    const wrapper = mount(Badge, {
      props: {
        color: {
          text: '#123456',
          bg: '#eef6fb',
          border: '#8fb6ca',
        },
      },
    })

    expect(wrapper.attributes('style')).toContain('--badge-text: #123456')
    expect(wrapper.attributes('style')).toContain('--badge-bg: #eef6fb')
    expect(wrapper.attributes('style')).toContain('--badge-border: #8fb6ca')
  })
})
