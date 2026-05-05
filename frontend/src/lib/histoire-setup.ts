import './theme.css'

// Mirror the .dark class to <html> so Teleport targets (Dialog, Toast)
// inherit dark-mode CSS variables even when Histoire applies .dark to
// an inner story wrapper instead of the document root.
function syncDarkToHtml(root: Element) {
  if (root.classList.contains('dark')) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

if (typeof document !== 'undefined') {
  const observer = new MutationObserver((mutations) => {
    for (const m of mutations) {
      if (m.type === 'attributes' && m.attributeName === 'class') {
        syncDarkToHtml(m.target as Element)
      }
    }
  })

  document.addEventListener('DOMContentLoaded', () => {
    const storyRoot = document.querySelector('#app') ?? document.body
    syncDarkToHtml(storyRoot)
    observer.observe(storyRoot, { attributes: true })
  })
}

export function setupVue3() {}

export function setupVanilla() {}
