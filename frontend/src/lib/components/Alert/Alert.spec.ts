import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Alert from './Alert.vue'

describe('Alert', () => {
  it('renders title', () => {
    const wrapper = mount(Alert, { props: { title: 'Stream healthy', variant: 'ok' } })

    expect(wrapper.find('strong').text()).toBe('Stream healthy')
  })

  it('renders slot content', () => {
    const wrapper = mount(Alert, {
      props: { title: 'Note', variant: 'ok' },
      slots: { default: 'All nodes synced.' },
    })

    expect(wrapper.text()).toContain('All nodes synced.')
  })

  it('applies ok variant classes', () => {
    const wrapper = mount(Alert, { props: { title: 'OK', variant: 'ok' } })

    expect(wrapper.classes()).toContain('border-ok/50')
    expect(wrapper.classes()).toContain('text-ok')
  })

  it('applies info variant classes', () => {
    const wrapper = mount(Alert, { props: { title: 'Info', variant: 'info' } })

    expect(wrapper.classes()).toContain('border-info/50')
    expect(wrapper.classes()).toContain('text-info')
  })

  it('applies warn variant classes', () => {
    const wrapper = mount(Alert, { props: { title: 'Warn', variant: 'warn' } })

    expect(wrapper.classes()).toContain('text-warn')
  })

  it('applies err variant classes', () => {
    const wrapper = mount(Alert, { props: { title: 'Err', variant: 'err' } })

    expect(wrapper.classes()).toContain('text-err')
  })

  it('applies dim variant classes', () => {
    const wrapper = mount(Alert, { props: { title: 'Dim', variant: 'dim' } })

    expect(wrapper.classes()).toContain('border-border')
    expect(wrapper.classes()).toContain('text-text-lo')
  })
})
