import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'

import Pagination from './Pagination.vue'
import Table from './Table.vue'

const columns = [
  { key: 'ts', label: 'Timestamp', sortable: true },
  { key: 'id', label: 'Identity' },
  { key: 'result', label: 'Result' },
]

const rows = [
  { ts: '14:41:18', id: '張小明', result: 'Granted' },
  { ts: '14:40:31', id: 'Unknown', result: 'Denied' },
]

describe('Table', () => {
  it('renders column headers', () => {
    const wrapper = mount(Table, { props: { columns, rows } })
    expect(wrapper.text()).toContain('Timestamp')
    expect(wrapper.text()).toContain('Identity')
  })

  it('renders row data', () => {
    const wrapper = mount(Table, { props: { columns, rows } })
    expect(wrapper.text()).toContain('張小明')
    expect(wrapper.text()).toContain('Unknown')
  })

  it('emits sort event when sortable header clicked', async () => {
    const wrapper = mount(Table, { props: { columns, rows } })
    await wrapper.find('[data-sort-btn]').trigger('click')
    expect(wrapper.emitted('sort')?.[0]).toBeTruthy()
  })

  it('renders cell slot for custom rendering', () => {
    const wrapper = mount(Table, {
      props: { columns, rows },
      slots: { 'cell-result': '<span data-test="custom">Custom</span>' },
    })
    expect(wrapper.find('[data-test="custom"]').exists()).toBe(true)
  })
})

describe('Pagination', () => {
  it('renders page info', () => {
    const wrapper = mount(Pagination, { props: { page: 1, pageSize: 10, total: 128 } })
    expect(wrapper.text()).toContain('128')
  })

  it('emits page-change on next click', async () => {
    const wrapper = mount(Pagination, { props: { page: 1, pageSize: 10, total: 50 } })
    await wrapper.find('[data-next]').trigger('click')
    expect(wrapper.emitted('update:page')?.[0]).toEqual([2])
  })

  it('emits page-change on prev click', async () => {
    const wrapper = mount(Pagination, { props: { page: 3, pageSize: 10, total: 50 } })
    await wrapper.find('[data-prev]').trigger('click')
    expect(wrapper.emitted('update:page')?.[0]).toEqual([2])
  })

  it('disables prev on first page', () => {
    const wrapper = mount(Pagination, { props: { page: 1, pageSize: 10, total: 50 } })
    expect(wrapper.find('[data-prev]').attributes('disabled')).toBeDefined()
  })

  it('disables next on last page', () => {
    const wrapper = mount(Pagination, { props: { page: 5, pageSize: 10, total: 50 } })
    expect(wrapper.find('[data-next]').attributes('disabled')).toBeDefined()
  })
})
