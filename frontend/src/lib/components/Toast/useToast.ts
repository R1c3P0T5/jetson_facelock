import { computed, reactive } from 'vue'

interface ToastEntry {
  id: number
  title: string
  message?: string
  duration: number
}

interface ToastOptions {
  title: string
  message?: string
  duration?: number
}

let nextId = 0
const state = reactive<{ entries: ToastEntry[] }>({ entries: [] })

export function _resetToast() {
  state.entries = []
  nextId = 0
}

export function useToast() {
  const toasts = computed(() => state.entries)

  function show(options: ToastOptions) {
    const id = nextId++
    const entry: ToastEntry = {
      id,
      title: options.title,
      message: options.message,
      duration: options.duration ?? 2300,
    }
    state.entries.push(entry)
    setTimeout(() => hide(id), entry.duration)
  }

  function hide(id: number) {
    const idx = state.entries.findIndex((e) => e.id === id)
    if (idx !== -1) state.entries.splice(idx, 1)
  }

  return { toasts, show, hide }
}
