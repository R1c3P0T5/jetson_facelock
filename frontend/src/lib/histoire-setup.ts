import './theme.css'

// Histoire applies the `dark` class to an inner story preview container,
// not to <html>. Vue Teleport (Dialog, Toast) renders directly into
// document.body, which sits outside that container — so teleported
// elements don't inherit dark-mode CSS variables via normal DOM cascade.
//
// Fix: watch the entire body subtree for `.dark` and mirror the state
// onto document.documentElement so that all content, including teleported
// nodes, inherits the correct color-scheme tokens.
if (typeof document !== 'undefined') {
  const html = document.documentElement

  const sync = () => {
    const hasDark = !!document.querySelector('.dark:not(html)')
    html.classList.toggle('dark', hasDark)
  }

  const observer = new MutationObserver(sync)

  const start = () => {
    sync()
    observer.observe(document.body, {
      attributes: true,
      attributeFilter: ['class'],
      subtree: true,
    })
  }

  if (document.body) {
    start()
  } else {
    document.addEventListener('DOMContentLoaded', start)
  }
}

export function setupVue3() {}

export function setupVanilla() {}
