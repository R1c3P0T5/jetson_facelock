import { mount } from '@vue/test-utils'
import { afterEach, describe, expect, it } from 'vitest'

import Dialog from './Dialog.vue'

describe('Dialog', () => {
  const wrappers: ReturnType<typeof mount>[] = []

  afterEach(() => {
    wrappers.forEach((w) => w.unmount())
    wrappers.length = 0
  })

  it('is hidden when open is false', () => {
    const wrapper = mount(Dialog, { props: { open: false, title: 'Confirm' } })
    wrappers.push(wrapper)
    expect(wrapper.find('[role="dialog"]').exists()).toBe(false)
  })

  it('is visible when open is true', () => {
    const wrapper = mount(Dialog, {
      props: { open: true, title: 'Confirm' },
      attachTo: document.body,
    })
    wrappers.push(wrapper)
    expect(document.body.querySelector('[role="dialog"]')).not.toBeNull()
  })

  it('renders title', () => {
    const wrapper = mount(Dialog, {
      props: { open: true, title: 'Apply policy update?' },
      attachTo: document.body,
    })
    wrappers.push(wrapper)
    expect(document.body.querySelector('[role="dialog"]')?.textContent).toContain(
      'Apply policy update?',
    )
  })

  it('renders default slot content', () => {
    const wrapper = mount(Dialog, {
      props: { open: true, title: 'Confirm' },
      slots: { default: '<p>Body content</p>' },
      attachTo: document.body,
    })
    wrappers.push(wrapper)
    expect(document.body.textContent).toContain('Body content')
  })

  it('emits update:open with false when backdrop is clicked', async () => {
    const wrapper = mount(Dialog, {
      props: { open: true, title: 'Confirm' },
      attachTo: document.body,
    })
    wrappers.push(wrapper)
    const backdrop = document.body.querySelector('[data-backdrop]') as HTMLElement
    backdrop.click()
    await Promise.resolve()
    expect(wrapper.emitted('update:open')?.[0]).toEqual([false])
  })
})
