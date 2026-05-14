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
          K-cinema
        </span>
      </RouterLink>

      <nav class="flex flex-wrap items-center justify-end gap-1 sm:gap-2">
        <RouterLink
          to="/"
          class="rounded-lg px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-200/90 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-white"
          active-class="!bg-white !text-violet-800 shadow-sm ring-1 ring-slate-300/80 dark:!bg-violet-950/50 dark:!text-violet-200 dark:ring-slate-700"
        >
          Main
        </RouterLink>
        
        <RouterLink v-if="auth.isAdmin"
          to="/create"
          class="rounded-lg px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-200/90 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-white"
          active-class="!bg-white !text-violet-800 shadow-sm ring-1 ring-slate-300/80 dark:!bg-violet-950/50 dark:!text-violet-200 dark:ring-slate-700"
        >
          Add film
        </RouterLink>

        <template v-if="auth.isAuthenticated">
        <router-link
          to="/profile/tickets"
          class="group flex items-center gap-2 rounded-xl bg-white px-3 py-1.5 text-xs font-bold text-slate-700 ring-1 ring-slate-300/80 transition-all hover:bg-slate-50 hover:ring-violet-500/50 dark:bg-slate-800 dark:text-slate-200 dark:ring-slate-700 dark:hover:bg-slate-700/50"
          :title="'My Tickets: ' + auth.username"
        >
          <span class="text-base transition-transform group-hover:rotate-12">🎫</span>
          
          <span class="hidden max-w-32 truncate sm:inline">
            {{ auth.username }}
          </span>
        </router-link>

        <button
          type="button"
          class="rounded-xl px-3 py-2 text-sm font-semibold text-slate-500 transition-colors hover:bg-red-50 hover:text-red-600 dark:text-slate-400 dark:hover:bg-red-950/30 dark:hover:text-red-400"
          @click="logout"
        >
          logout
        </button>
      </template>

      <template v-else>
        <button
          type="button"
          class="rounded-xl bg-violet-600 px-5 py-2 text-sm font-bold text-white shadow-lg shadow-violet-500/20 transition-all hover:bg-violet-500 hover:shadow-violet-500/40"
          @click="auth.openAuthModal('login')"
        >
          Sign In
        </button>
      </template>

        <ThemeToggle />
      </nav>
    </div>
  </header>
</template>
