import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Button from './Button.vue'

describe('Button', () => {
  it('renders slot content', () => {
    const wrapper = mount(Button, { slots: { default: 'Click me' } })
    expect(wrapper.text()).toBe('Click me')
  })

  it('renders as a <button> element', () => {
    const wrapper = mount(Button)
    expect(wrapper.element.tagName).toBe('BUTTON')
  })

  it('applies primary variant class', () => {
    const wrapper = mount(Button, { props: { variant: 'primary' } })
    expect(wrapper.classes()).toContain('bg-ac')
  })

  it('applies ok variant classes', () => {
    const wrapper = mount(Button, { props: { variant: 'ok' } })

    expect(wrapper.classes()).toContain('text-ok')
    expect(wrapper.classes()).toContain('border-ok/50')
  })

  it('applies info variant classes', () => {
    const wrapper = mount(Button, { props: { variant: 'info' } })

    expect(wrapper.classes()).toContain('text-info')
    expect(wrapper.classes()).toContain('border-info/50')
  })

  it('applies warn variant classes', () => {
    const wrapper = mount(Button, { props: { variant: 'warn' } })

    expect(wrapper.classes()).toContain('text-warn')
    expect(wrapper.classes()).toContain('border-warn/50')
  })

  it('applies err variant class', () => {
    const wrapper = mount(Button, { props: { variant: 'err' } })
    expect(wrapper.classes()).toContain('text-err')
  })

  it('applies xs size class', () => {
    const wrapper = mount(Button, { props: { size: 'xs' } })
    expect(wrapper.classes()).toContain('min-h-[28px]')
  })

  it('applies distinct sm size classes', () => {
    const wrapper = mount(Button, { props: { size: 'sm' } })

    expect(wrapper.classes()).toContain('min-h-[32px]')
    expect(wrapper.classes()).toContain('text-[11px]')
  })

  it('applies compact xs classes for tool buttons', () => {
    const wrapper = mount(Button, { props: { size: 'xs' }, slots: { default: 'x' } })

    expect(wrapper.classes()).toContain('min-h-[28px]')
    expect(wrapper.classes()).toContain('px-2')
  })

  it('applies custom color styles', () => {
    const wrapper = mount(Button, {
      props: {
        color: {
          text: '#f8fbfd',
          bg: '#326f91',
          border: '#326f91',
          hoverBg: '#245a76',
          hoverBorder: '#245a76',
        },
      },
    })

    expect(wrapper.attributes('style')).toContain('--button-text: #f8fbfd')
    expect(wrapper.attributes('style')).toContain('--button-bg: #326f91')
    expect(wrapper.classes()).toContain('text-[var(--button-text)]')
  })

  it('sets disabled attribute when disabled prop is true', () => {
    const wrapper = mount(Button, { props: { disabled: true } })
    expect((wrapper.element as HTMLButtonElement).disabled).toBe(true)
  })

  it('shows loading indicator and sets aria-busy when loading', () => {
    const wrapper = mount(Button, { props: { loading: true } })
    expect(wrapper.find('[aria-hidden="true"]').exists()).toBe(true)
    expect(wrapper.attributes('aria-busy')).toBe('true')
  })

  it('is disabled when loading', () => {
    const wrapper = mount(Button, { props: { loading: true } })
    expect((wrapper.element as HTMLButtonElement).disabled).toBe(true)
  })
})
