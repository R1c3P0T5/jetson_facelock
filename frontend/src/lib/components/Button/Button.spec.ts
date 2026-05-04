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

  it('applies danger variant class', () => {
    const wrapper = mount(Button, { props: { variant: 'danger' } })
    expect(wrapper.classes()).toContain('text-err')
  })

  it('applies xs size class', () => {
    const wrapper = mount(Button, { props: { size: 'xs' } })
    expect(wrapper.classes()).toContain('min-h-[30px]')
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
