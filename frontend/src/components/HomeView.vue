<script setup lang="ts">
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useMovieStore } from '@/stores/Movie'
import MovieCard from './MovieCard.vue'
import AppHeader from './AppHeader.vue'

const store = useMovieStore()

onMounted(() => {
  void store.getMovies()
})
</script>

<template>
  <div class="flex min-h-screen flex-col">
    <AppHeader />

    <main class="flex-1">
      <!-- hero -->
      <section
        class="relative overflow-hidden border-b border-slate-300/80 bg-slate-100/40 dark:border-slate-800/80 dark:bg-transparent"
      >
        <div
          class="pointer-events-none absolute -left-24 top-0 h-72 w-72 rounded-full bg-violet-400/12 blur-3xl dark:bg-violet-600/20"
        />
        <div
          class="pointer-events-none absolute -right-20 top-24 h-64 w-64 rounded-full bg-fuchsia-400/10 blur-3xl dark:bg-fuchsia-600/15"
        />
        <div
          class="pointer-events-none absolute bottom-0 left-1/2 h-40 w-[120%] -translate-x-1/2 bg-gradient-to-t from-slate-200/95 to-transparent dark:from-slate-950/90"
        />

        <div class="relative mx-auto max-w-6xl px-4 pb-14 pt-10 sm:px-6 sm:pb-16 sm:pt-14">
          <p
            class="mb-3 inline-flex items-center rounded-full border border-violet-300/70 bg-white/80 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-violet-800 shadow-sm dark:border-violet-500/30 dark:bg-violet-950/50 dark:text-violet-300 dark:shadow-none"
          >
            Сегодня в кино
          </p>
          <h1
            class="max-w-2xl text-4xl font-extrabold tracking-tight text-slate-800 sm:text-5xl dark:text-white"
          >
            Выберите фильм
            <span class="bg-gradient-to-r from-violet-600 to-fuchsia-600 bg-clip-text text-transparent dark:from-violet-400 dark:to-fuchsia-400">
              и места
            </span>
          </h1>
          <p class="mt-4 max-w-xl text-lg text-slate-700 dark:text-slate-400">
            Афиша кинотеатра: постер, описание и бронирование мест в пару кликов.
          </p>
          <div class="mt-8 flex flex-wrap gap-3">
            <RouterLink
              to="/create"
              class="inline-flex items-center justify-center rounded-xl bg-gradient-to-r from-violet-600 to-fuchsia-600 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-violet-500/25 transition hover:shadow-xl hover:shadow-violet-500/35"
            >
              Добавить фильм
            </RouterLink>
            <span
              class="inline-flex items-center rounded-xl border border-slate-300/90 bg-white px-4 py-2.5 text-sm font-medium text-slate-700 shadow-sm dark:border-slate-700 dark:bg-slate-900/60 dark:text-slate-300 dark:shadow-none"
            >
              {{ store.movies.length }} в афише
            </span>
          </div>
        </div>
      </section>

      <!-- grid -->
      <section class="mx-auto max-w-6xl px-4 py-12 sm:px-6 sm:py-16">
        <div class="mb-8 flex flex-wrap items-end justify-between gap-4">
          <div>
            <h2 class="text-2xl font-bold text-slate-800 dark:text-white">
              Сейчас в прокате
            </h2>
            <p class="mt-1 text-sm text-slate-600 dark:text-slate-400">
              Нажмите на карточку, чтобы выбрать места в зале.
            </p>
          </div>
        </div>

        <div v-if="store.loading" class="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 md:gap-6">
          <div
            v-for="n in 8"
            :key="n"
            class="aspect-[2/3] animate-pulse rounded-2xl bg-slate-300/70 dark:bg-slate-800/80"
          />
        </div>

        <template v-else>
          <div
            v-if="store.movies.length === 0"
            class="rounded-2xl border border-dashed border-slate-400/70 bg-white/70 px-6 py-16 text-center shadow-sm dark:border-slate-600 dark:bg-slate-900/40 dark:shadow-none"
          >
            <p class="text-4xl">🎬</p>
            <p class="mt-4 text-lg font-semibold text-slate-800 dark:text-slate-100">
              Афиша пока пустая
            </p>
            <p class="mx-auto mt-2 max-w-md text-slate-600 dark:text-slate-400">
              Запустите бэкенд, проверьте базу или добавьте первый фильм.
            </p>
            <RouterLink
              to="/create"
              class="mt-6 inline-flex rounded-xl bg-violet-600 px-5 py-2.5 text-sm font-semibold text-white shadow-md transition hover:bg-violet-500"
            >
              Добавить фильм
            </RouterLink>
          </div>

          <div
            v-else
            class="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 md:gap-6"
          >
            <RouterLink
              v-for="m in store.movies"
              :key="m.id"
              :to="`/booking/${m.id}`"
              class="group block rounded-2xl outline-none ring-offset-2 ring-offset-slate-100 transition hover:-translate-y-1 focus-visible:ring-2 focus-visible:ring-violet-600 dark:ring-offset-slate-950"
            >
              <MovieCard :movie="m" />
            </RouterLink>
          </div>
        </template>
      </section>
    </main>

    <footer
      class="border-t border-slate-300/80 py-8 text-center text-sm text-slate-600 dark:border-slate-800 dark:text-slate-400"
    >
      Kinoteatr · курсовой проект
    </footer>
  </div>
</template>
