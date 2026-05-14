<script setup lang="ts">
import { RouterLink } from 'vue-router'
import ThemeToggle from './themeToggle.vue'
import { userStore } from '@/stores/user'

const auth = userStore()

function logout() {
  auth.logout()
}
</script>

<template>
  <header
    class="sticky top-0 z-40 border-b border-slate-300/90 bg-slate-100/95 shadow-sm backdrop-blur-md dark:border-slate-800/80 dark:bg-slate-950/90"
  >
    <div class="mx-auto flex h-14 max-w-6xl items-center justify-between gap-3 px-4 sm:h-16 sm:px-6">
      <RouterLink
        to="/"
        class="group flex items-center gap-2.5 rounded-lg outline-none ring-violet-500/0 transition focus-visible:ring-2 focus-visible:ring-violet-500 focus-visible:ring-offset-2 focus-visible:ring-offset-slate-100 dark:focus-visible:ring-offset-slate-950"
      >
        <span
          class="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-violet-600 to-fuchsia-600 text-sm font-black text-white shadow-md shadow-violet-600/20 transition group-hover:shadow-lg dark:shadow-violet-500/25"
        >
          K
        </span>
        <span class="hidden text-lg font-bold tracking-tight text-slate-800 sm:inline dark:text-white">
          Kinoteatr
        </span>
      </RouterLink>

      <nav class="flex flex-wrap items-center justify-end gap-1 sm:gap-2">
        <RouterLink
          to="/"
          class="rounded-lg px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-200/90 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-white"
          active-class="!bg-white !text-violet-800 shadow-sm ring-1 ring-slate-300/80 dark:!bg-violet-950/50 dark:!text-violet-200 dark:ring-slate-700"
        >
          Главная
        </RouterLink>
        <RouterLink
          to="/create"
          class="rounded-lg px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-200/90 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-white"
          active-class="!bg-white !text-violet-800 shadow-sm ring-1 ring-slate-300/80 dark:!bg-violet-950/50 dark:!text-violet-200 dark:ring-slate-700"
        >
          Новый фильм
        </RouterLink>

        <template v-if="auth.isAuthenticated">
          <span
            class="hidden max-w-40 truncate rounded-lg bg-white px-2.5 py-1.5 text-xs font-medium text-slate-700 ring-1 ring-slate-300/80 sm:inline dark:bg-slate-800 dark:text-slate-200 dark:ring-slate-600"
            :title="auth.username"
          >
            {{ auth.username }}
          </span>
          <button
            type="button"
            class="rounded-lg px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-200/90 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-white"
            @click="logout"
          >
            Выйти
          </button>
        </template>
        <template v-else>
          <button
            type="button"
            class="rounded-lg px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-200/90 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-white"
            @click="auth.openAuthModal('login')"
          >
            Auth
          </button>
          
        </template>

        <ThemeToggle />
      </nav>
    </div>
  </header>
</template>
