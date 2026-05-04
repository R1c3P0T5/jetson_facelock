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

  it('renders without a title', () => {
    const wrapper = mount(Alert, {
      props: { variant: 'info' },
      slots: { default: 'Body only message.' },
    })

    expect(wrapper.find('strong').exists()).toBe(false)
    expect(wrapper.text()).toBe('Body only message.')
  })

  it('renders icon slot before title', () => {
    const wrapper = mount(Alert, {
      props: { title: 'Model updated', variant: 'info' },
      slots: { icon: '<span data-test="alert-icon">i</span>' },
    })

    const header = wrapper.find('[data-test="alert-header"]')

    expect(header.element.firstElementChild).toBe(wrapper.find('[data-test="alert-icon"]').element)
    expect(header.find('strong').text()).toBe('Model updated')
  })

  it('renders no close button by default', () => {
    const wrapper = mount(Alert, { props: { title: 'Note', variant: 'info' } })

    expect(wrapper.find('button').exists()).toBe(false)
  })

  it('emits close and hides alert when close button is clicked', async () => {
    const wrapper = mount(Alert, { props: { title: 'Note', variant: 'info', closable: true } })

    await wrapper.find('button').trigger('click')

    expect(wrapper.emitted('close')).toHaveLength(1)
    expect(wrapper.find('[role="alert"]').exists()).toBe(false)
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
