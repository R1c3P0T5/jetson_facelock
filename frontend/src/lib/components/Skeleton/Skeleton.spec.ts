import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Skeleton from './Skeleton.vue'

describe('Skeleton', () => {
  it('renders with default height', () => {
    const wrapper = mount(Skeleton)
    expect(wrapper.attributes('style')).toContain('height: 14px')
  })

  it('applies custom height', () => {
    const wrapper = mount(Skeleton, { props: { height: 88 } })
    expect(wrapper.attributes('style')).toContain('height: 88px')
  })

  it('applies string height', () => {
    const wrapper = mount(Skeleton, { props: { height: '3rem' } })
    expect(wrapper.attributes('style')).toContain('height: 3rem')
  })

  it('has role=status for accessibility', () => {
    const wrapper = mount(Skeleton)
    expect(wrapper.attributes('role')).toBe('status')
  })
})
