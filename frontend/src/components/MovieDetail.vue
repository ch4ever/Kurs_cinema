<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMovieStore } from '@/stores/Movie'
import { userStore } from '@/stores/user'
import AppHeader from './AppHeader.vue'

const route = useRoute()
const router = useRouter()
const movieStore = useMovieStore()
const auth = userStore()

const movieId = Number(route.params.id)

onMounted(() => {
  void movieStore.getMovie(movieId)
})

const movie = computed(() => movieStore.movie)

const goToBooking = () => {
  router.push(`/booking/${movieId}`)
}

const goToEdit = () => {
  router.push(`/edit/${movieId}`)
}
</script>

<template>
  <div class="min-h-screen bg-slate-50 dark:bg-[#0B0F19] transition-colors duration-300">
    <AppHeader />

    <div v-if="movieStore.loading" class="flex h-[80vh] items-center justify-center">
      <div class="h-12 w-12 animate-spin rounded-full border-4 border-violet-500 border-t-transparent"></div>
    </div>

    <main v-else-if="movie" class="relative">
      
      <div class="absolute inset-0 h-[60vh] overflow-hidden">
        <img 
          v-if="movie.poster" 
          :src="movie.poster" 
          class="h-full w-full object-cover opacity-20 blur-3xl saturate-150"
        />
        <div class="absolute inset-0 bg-gradient-to-b from-transparent via-slate-50 to-slate-50 dark:via-[#0B0F19] dark:to-[#0B0F19]"></div>
      </div>

      <div class="relative mx-auto max-w-6xl px-4 pt-12 pb-24 sm:px-6 lg:px-8">
        <div class="flex flex-col gap-10 lg:flex-row">
          
          <div class="mx-auto w-full max-w-[320px] lg:mx-0 flex-shrink-0">
            <div class="group relative aspect-[2/3] overflow-hidden rounded-3xl shadow-2xl ring-1 ring-white/20">
              <img 
                v-if="movie.poster" 
                :src="movie.poster" 
                :alt="movie.title"
                class="h-full w-full object-cover transition duration-500 group-hover:scale-105"
              />
              <div v-else class="flex h-full w-full items-center justify-center bg-slate-200 dark:bg-slate-800">
                <span class="text-6xl text-slate-400">🎬</span>
              </div>
              
              <button
                v-if="auth.isAdmin"
                @click="goToEdit"
                class="absolute top-4 right-4 flex h-12 w-12 items-center justify-center rounded-full bg-white/10 backdrop-blur-md text-white shadow-xl transition hover:bg-violet-600"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125" />
                </svg>
              </button>
            </div>
          </div>

          <div class="flex flex-col">
            <div class="mb-4 flex flex-wrap gap-2">
              <span class="inline-flex items-center rounded-md bg-violet-500/10 px-2 py-1 text-xs font-bold uppercase tracking-wider text-violet-600 ring-1 ring-inset ring-violet-500/20 dark:text-violet-400">
                Full HD
              </span>
              <!-- <span class="inline-flex items-center rounded-md bg-amber-500/10 px-2 py-1 text-xs font-bold uppercase tracking-wider text-amber-600 ring-1 ring-inset ring-amber-500/20 dark:text-amber-400">
                IMDb {{ movie.rating || 'N/A' }}
              </span> -->
            </div>

            <h1 class="text-4xl font-extrabold tracking-tight text-slate-900 sm:text-6xl dark:text-white">
              {{ movie.title }}
            </h1>

            <div class="mt-6 flex flex-wrap items-center gap-6 text-sm font-medium text-slate-500 dark:text-slate-400">
              <div class="flex items-center gap-1">
                <span>📅</span>
                {{ new Date(movie.release_date).getFullYear() }}
              </div>
              <div class="flex items-center gap-1">
                <span>⏱️</span>
                <!-- TODO FIX LATER -->
                <!-- {{ movie.duration || 120 }} min -->120
              </div>
              <div class="flex items-center gap-1">
                <span>🎭</span>
                {{ movie.director || 'Unknown' }}
              </div>
            </div>

            <div class="mt-10">
              <h3 class="text-lg font-bold text-slate-900 dark:text-white">Synopsis</h3>
              <p class="mt-3 max-w-3xl text-lg leading-relaxed text-slate-600 dark:text-slate-400">
                {{ movie.description }}
              </p>
            </div>

            <div v-if="movie.actors && movie.actors.length > 0" class="mt-10">
              <h3 class="text-lg font-bold text-slate-900 dark:text-white mb-4">Cast</h3>
              <div class="flex flex-wrap gap-3">
                <div v-for="actor in movie.actors" :key="actor.id" class="rounded-full bg-white px-4 py-2 text-sm font-semibold shadow-sm ring-1 ring-slate-200 dark:bg-slate-800 dark:ring-slate-700 dark:text-slate-200">
                  {{ actor.name }}
                </div>
              </div>
            </div>

            <div class="mt-12 flex flex-wrap gap-4">
              <button
                @click="goToBooking"
                class="inline-flex items-center justify-center rounded-2xl bg-gradient-to-r from-violet-600 to-fuchsia-600 px-10 py-4 text-lg font-bold text-white shadow-xl shadow-violet-500/25 transition-all hover:-translate-y-1 hover:shadow-violet-500/40"
              >
                🎟️ Book Tickets Now
              </button>
              
              <!-- <button
                class="inline-flex items-center justify-center rounded-2xl bg-white px-10 py-4 text-lg font-bold text-slate-900 shadow-sm ring-1 ring-slate-200 transition hover:bg-slate-50 dark:bg-slate-800 dark:text-white dark:ring-slate-700 dark:hover:bg-slate-700"
              >
                📽️ Watch Trailer
              </button> -->
            </div>
          </div>
        </div>
      </div>
    </main>

    <div v-else class="flex h-[60vh] flex-col items-center justify-center text-center">
      <span class="text-6xl">🏜️</span>
      <h2 class="mt-4 text-2xl font-bold text-slate-900 dark:text-white">Movie not found</h2>
      <p class="mt-2 text-slate-500">It might have been removed from the schedule.</p>
      <RouterLink to="/" class="mt-6 text-violet-500 font-bold hover:underline">Go back home</RouterLink>
    </div>
  </div>
</template>