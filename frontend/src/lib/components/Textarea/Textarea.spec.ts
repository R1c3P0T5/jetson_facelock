import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Textarea from './Textarea.vue'

describe('Textarea', () => {
  it('renders the current value', () => {
    const wrapper = mount(Textarea, { props: { modelValue: 'Device notes' } })

    expect((wrapper.find('textarea').element as HTMLTextAreaElement).value).toBe('Device notes')
  })

  it('emits update:modelValue on input', async () => {
    const wrapper = mount(Textarea, { props: { modelValue: '' } })

    await wrapper.find('textarea').setValue('Require supervisor approval')

    expect(wrapper.emitted('update:modelValue')?.[0]).toEqual(['Require supervisor approval'])
  })

  it('passes attributes to the textarea', () => {
    const wrapper = mount(Textarea, {
      props: { modelValue: '' },
      attrs: { placeholder: 'Add notes', rows: 6 },
    })
    const textarea = wrapper.find('textarea')

    expect(textarea.attributes('placeholder')).toBe('Add notes')
    expect(textarea.attributes('rows')).toBe('6')
  })

  it('applies invalid state from prop or aria-invalid attr', () => {
    const propWrapper = mount(Textarea, { props: { modelValue: '', invalid: true } })
    const attrWrapper = mount(Textarea, {
      props: { modelValue: '' },
      attrs: { 'aria-invalid': 'true' },
    })

    expect(propWrapper.find('textarea').classes()).toContain('border-err')
    expect(propWrapper.find('textarea').attributes('aria-invalid')).toBe('true')
    expect(attrWrapper.find('textarea').classes()).toContain('border-err')
  })

  it('renders error before hint when invalid', () => {
    const wrapper = mount(Textarea, {
      props: { modelValue: '', invalid: true, hint: 'Optional', error: 'Required' },
    })

    expect(wrapper.text()).toContain('Required')
    expect(wrapper.text()).not.toContain('Optional')
  })
})
