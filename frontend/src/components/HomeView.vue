<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useMovieStore } from '@/stores/Movie'
import MovieCard from './MovieCard.vue'
import AppHeader from './AppHeader.vue'
import { userStore } from '@/stores/user'

const store = useMovieStore()
const auth = userStore()

onMounted(() => {
  void store.fetchMovies()
})
</script>

<template>
  <div class="flex min-h-screen flex-col bg-slate-50 selection:bg-violet-500/30 dark:bg-[#0B0F19] transition-colors duration-300">
    <AppHeader />

    <main class="flex-1">
      <section class="relative overflow-hidden pt-16 pb-24 lg:pt-24 lg:pb-32">
        
        <div class="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80 pointer-events-none">
          <div 
            class="relative left-[calc(50%-11rem)] aspect-1155/678 w-144.5 -translate-x-1/2 rotate-30 bg-linear-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 dark:opacity-20 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]" 
            style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)">
          </div>
        </div>

        <div class="absolute inset-x-0 top-[calc(100%-13rem)] -z-10 transform-gpu overflow-hidden blur-3xl sm:top-[calc(100%-30rem)] pointer-events-none">
          <div 
            class="relative left-[calc(50%+3rem)] aspect-1155/678 w-144.5 -translate-x-1/2 bg-linear-to-tr from-[#ff80b5] to-[#9089fc] opacity-30 dark:opacity-20 sm:left-[calc(50%+36rem)] sm:w-[72.1875rem]" 
            style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)">
          </div>
        </div>

        <div class="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <div class="mb-6 inline-flex items-center justify-center rounded-full border border-violet-200 bg-white/60 px-4 py-1.5 text-sm font-semibold uppercase tracking-widest text-violet-700 backdrop-blur-md shadow-sm dark:border-violet-800/50 dark:bg-violet-900/20 dark:text-violet-300">
            <span class="mr-2 flex h-2 w-2 rounded-full bg-violet-500 animate-pulse"></span>
            Today in K-Cinema
          </div>

          <h1 class="mx-auto max-w-4xl text-5xl font-extrabold tracking-tight text-slate-900 sm:text-7xl dark:text-white">
            Choose the films
            <span class="relative whitespace-nowrap text-transparent bg-clip-text bg-linear-to-r from-violet-600 to-fuchsia-600 dark:from-violet-400 dark:to-fuchsia-400">
              <svg aria-hidden="true" viewBox="0 0 418 42" class="absolute left-0 top-2/3 h-[0.58em] w-full fill-violet-300/50 dark:fill-violet-700/50" preserveAspectRatio="none"><path d="M203.371.916c-26.013-2.078-76.686 1.963-124.738 9.423-9.293 1.43-34.614 5.244-48.423 8.358-13.808 3.113-28.536 7.42-30.124 7.646-1.587.225-2.28 1.472-1.408 2.544.872 1.073 5.434 1.343 11.236.666 4.67-.543 14.864-2.583 22.651-4.542 56.402-14.167 116.516-19.658 174.551-15.918 41.59 2.682 82.547 11.455 120.301 25.801 10.975 4.167 31.968 13.064 33.25 14.184 1.282 1.121 2.378-.458 1.543-2.222-2.146-4.521-12.78-14.398-22.186-20.655C310.222 9.07 258.91 3.268 203.371.916z"></path></svg>
              <span class="relative">and the places</span>
            </span>
          </h1>

          <p class="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-600 dark:text-slate-400">
            K-Cinema, may the films be with you.
          </p>

          <div class="mt-10 flex items-center justify-center gap-4 flex-wrap">
            <RouterLink
              v-if="auth.isAdmin"
              to="/create"
              class="group relative inline-flex items-center justify-center rounded-xl bg-violet-600 px-8 py-3.5 text-base font-semibold text-white shadow-lg shadow-violet-500/30 transition-all hover:-translate-y-0.5 hover:bg-violet-500 hover:shadow-violet-500/40 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-violet-600"
            >
              <span class="mr-2">➕</span> Add Movie
            </RouterLink>

            <div class="inline-flex items-center gap-x-2 rounded-xl bg-white/50 px-6 py-3.5 text-base font-medium text-slate-700 ring-1 ring-inset ring-slate-200/50 backdrop-blur-md dark:bg-slate-800/50 dark:text-slate-300 dark:ring-slate-700/50 cursor-default">
              <span>🍿</span>
              {{ store.movies.length }} in theaters
            </div>
          </div>
        </div>
      </section>

      <section class="mx-auto max-w-7xl px-4 pb-20 sm:px-6 lg:px-8">
        
        <div class="mb-10 flex flex-col sm:flex-row items-center justify-between border-b border-slate-200 pb-6 dark:border-slate-800">
          <div>
            <h2 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
              Now available
            </h2>
            <p class="mt-2 text-sm text-slate-500 dark:text-slate-400">
              Click on card to chose your position.
            </p>
          </div>
        </div>

        <div v-if="store.loading" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 lg:gap-8">
          <div
            v-for="n in 8"
            :key="n"
            class="aspect-2/3 w-full animate-pulse rounded-2xl bg-slate-200 dark:bg-slate-800/80"
          ></div>
        </div>

        <template v-else>
          <div
            v-if="store.movies.length === 0"
            class="flex flex-col items-center justify-center rounded-3xl border-2 border-dashed border-slate-300 bg-slate-50/50 px-6 py-24 text-center dark:border-slate-700 dark:bg-slate-900/50 transition-colors"
          >
            <div class="flex h-20 w-20 items-center justify-center rounded-full bg-violet-100 dark:bg-violet-900/30">
              <span class="text-4xl drop-shadow-md">🎬</span>
            </div>
            <h3 class="mt-6 text-xl font-semibold text-slate-900 dark:text-white">Empty...</h3>
            <p class="mt-2 text-slate-500 dark:text-slate-400 max-w-sm">
              No films here yet...
            </p>
            <RouterLink
              v-if="auth.isAdmin"
              to="/create"
              class="mt-8 inline-flex items-center justify-center rounded-xl bg-violet-600 px-6 py-3 text-sm font-semibold text-white shadow-sm transition-all hover:bg-violet-500 hover:-translate-y-0.5 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-violet-600"
            >
              Add film
            </RouterLink>
          </div>

          <div
            v-else
            class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 lg:gap-8"
          >
            <RouterLink
              v-for="m in store.movies"
              :key="m.id"
              :to="`/movie/${m.id}`"
              class="group block outline-none transition-transform duration-300 hover:-translate-y-2 focus-visible:ring-4 focus-visible:ring-violet-500 focus-visible:ring-offset-4 focus-visible:ring-offset-slate-50 dark:focus-visible:ring-offset-slate-950 rounded-2xl"
            >
              <MovieCard :movie="m" />
            </RouterLink>
          </div>
        </template>
      </section>
    </main>

    <footer class="mt-auto py-8 border-t border-slate-200/60 bg-white/50 backdrop-blur-md dark:border-slate-800/60 dark:bg-slate-950/50 transition-colors">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center flex flex-col items-center justify-center">
        <p class="text-sm font-medium text-slate-500 dark:text-slate-400">
          © {{ new Date().getFullYear() }} Kinoteatr · Курсовой проект
        </p>
      </div>
    </footer>
  </div>
</template>