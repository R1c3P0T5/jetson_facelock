import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import State from './State.vue'

describe('State', () => {
  it('renders title', () => {
    const wrapper = mount(State, { props: { title: 'No records found' } })
    expect(wrapper.text()).toContain('No records found')
  })

  it('renders default slot content', () => {
    const wrapper = mount(State, {
      props: { title: 'Empty' },
      slots: { default: '<p>Try again</p>' },
    })
    expect(wrapper.text()).toContain('Try again')
  })

  it('applies error variant styles', () => {
    const wrapper = mount(State, { props: { title: 'Error', variant: 'error' } })
    expect(wrapper.classes().some((c) => c.includes('border-err'))).toBe(true)
  })

  it('applies centered layout when center prop is true', () => {
    const wrapper = mount(State, { props: { title: 'Empty', center: true } })
    expect(wrapper.classes().some((c) => c.includes('items-center'))).toBe(true)
  })
})
