import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Avatar from './Avatar.vue'
import AvatarStack from './AvatarStack.vue'

describe('Avatar', () => {
  it('renders initials', () => {
    const wrapper = mount(Avatar, { props: { initials: 'LW' } })
    expect(wrapper.text()).toBe('LW')
  })

  it('renders img when src provided', () => {
    const wrapper = mount(Avatar, { props: { initials: 'LW', src: '/photo.jpg' } })
    const img = wrapper.find('img')
    expect(img.exists()).toBe(true)
    expect(img.attributes('src')).toBe('/photo.jpg')
    expect(img.attributes('alt')).toBe('LW')
  })

  it('applies size sm', () => {
    const wrapper = mount(Avatar, { props: { initials: 'AB', size: 'sm' } })
    expect(wrapper.classes().some((c) => c.includes('h-6'))).toBe(true)
  })
})

describe('AvatarStack', () => {
  it('renders slotted avatars', () => {
    const wrapper = mount(AvatarStack, {
      slots: { default: '<span class="av">A</span><span class="av">B</span>' },
    })
    expect(wrapper.findAll('.av')).toHaveLength(2)
  })
})
