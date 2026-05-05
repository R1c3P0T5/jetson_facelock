import { mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it } from 'vitest'

import Toast from './Toast.vue'
import { _resetToast, useToast } from './useToast'

describe('useToast', () => {
  beforeEach(() => _resetToast())

  it('show() adds a toast entry', () => {
    const toast = useToast()
    toast.show({ title: 'Saved' })
    const { toasts } = useToast()
    expect(toasts.value).toHaveLength(1)
    expect(toasts.value[0]!.title).toBe('Saved')
  })

  it('hide() removes the toast by id', () => {
    const toast = useToast()
    toast.show({ title: 'Hello' })
    const id = useToast().toasts.value[0]!.id
    toast.hide(id)
    expect(useToast().toasts.value).toHaveLength(0)
  })
})

describe('Toast (ToastHost)', () => {
  beforeEach(() => _resetToast())

  it('renders nothing when no toasts', () => {
    mount(Toast, { attachTo: document.body })
    expect(document.body.querySelector('[role="status"]')).toBeNull()
  })

  it('renders toast title when show() is called', () => {
    const toast = useToast()
    toast.show({ title: 'Settings saved' })
    mount(Toast, { attachTo: document.body })
    expect(document.body.querySelector('[role="status"]')?.textContent).toContain('Settings saved')
  })
})
