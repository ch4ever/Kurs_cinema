import { defineStore } from 'pinia'
import { ref } from 'vue'

function applyDomTheme(mode: 'light' | 'dark') {
  const root = document.documentElement
  if (mode === 'dark') {
    root.classList.add('dark')
    root.style.colorScheme = 'dark'
  } else {
    root.classList.remove('dark')
    root.style.colorScheme = 'light'
  }
}

function readStoredTheme(): 'light' | 'dark' | null {
  const v = localStorage.getItem('theme')
  return v === 'dark' || v === 'light' ? v : null
}

export const useUserSettingsStore = defineStore('userSettings', () => {
  const theme = ref<'light' | 'dark'>(
    readStoredTheme() ?? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'),
  )

  const setTheme = (newTheme: 'light' | 'dark') => {
    theme.value = newTheme
    localStorage.setItem('theme', newTheme)
    applyDomTheme(newTheme)
  }

  const changeTheme = () => {
    setTheme(theme.value === 'dark' ? 'light' : 'dark')
  }

  const initTheme = () => {
    applyDomTheme(theme.value)
  }

  return { theme, changeTheme, setTheme, initTheme }
})
