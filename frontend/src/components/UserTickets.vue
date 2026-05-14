<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import api from '@/api/api'
  import AppHeader from './AppHeader.vue'

  interface Ticket {
  id: number
  movie: {
    id: number
    title: string
    poster: string | null
    release_date: string
  }
  seats: string[] | string
  booked_at: string
}
  
const tickets = ref<Ticket[]>([])
  const loading = ref(true)
  
  onMounted(async () => {
    try {
      const { data } = await api.get<Ticket[]>('my-tickets/')
      tickets.value = data
    } catch (e) {
      console.error('Ошибка загрузки билетов', e)
    } finally {
      loading.value = false
    }
  })
  </script>

<template>
    <div class="min-h-screen bg-slate-50 dark:bg-[#0B0F19] transition-colors duration-300">
      <AppHeader />
  
      <main class="mx-auto max-w-4xl px-4 py-12">
        <div class="mb-10">
          <h1 class="text-4xl font-black text-slate-900 dark:text-white">My tickets</h1>
          <p class="text-slate-500 mt-2">Your active tickets.</p>
        </div>
  
        <div v-if="loading" class="space-y-4">
          <div v-for="i in 3" :key="i" class="h-32 w-full animate-pulse rounded-3xl bg-white dark:bg-slate-800/50"></div>
        </div>
  
        <div v-else-if="tickets.length === 0" class="text-center py-20 bg-white dark:bg-slate-900/40 rounded-[2.5rem] border-2 border-dashed border-slate-200 dark:border-slate-800">
          <span class="text-6xl block mb-4">🎟️</span>
          <h2 class="text-xl font-bold text-slate-900 dark:text-white">You dont have tickets yet</h2>
          <router-link to="/" class="mt-4 inline-block text-violet-500 font-bold hover:underline">Go to films</router-link>
        </div>
  
        <div v-else class="space-y-6">
          <div v-for="ticket in tickets" :key="ticket.id" 
               class="group relative overflow-hidden flex flex-col md:flex-row bg-white dark:bg-slate-900/60 rounded-3xl shadow-sm hover:shadow-md transition-all ring-1 ring-slate-200/50 dark:ring-white/5">
            
            <div class="w-full md:w-32 h-48 md:h-auto flex-shrink-0">
                <img 
                    v-if="ticket.movie.poster" 
                    :src="ticket.movie.poster" 
                    class="w-full h-full object-cover" 
                />
                <div v-else class="w-full h-full flex items-center justify-center bg-slate-200 dark:bg-slate-800">
                    <span>🎬</span>
                </div>
            </div>
  
            <div class="p-6 flex-grow flex flex-col justify-between">
              <div>
                <h3 class="text-xl font-black text-slate-900 dark:text-white group-hover:text-violet-600 transition-colors">
                  {{ ticket.movie.title }}
                </h3>
                <div class="mt-2 flex flex-wrap gap-x-4 gap-y-2 text-sm font-medium text-slate-500 dark:text-slate-400">
                  <span class="flex items-center gap-1">📅 {{ ticket.movie.release_date }}</span>
                  <span class="flex items-center gap-1">🕒 19:00</span> </div>
              </div>
  
              <div class="mt-4 pt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
                <div>
                  <p class="text-[10px] uppercase tracking-widest text-slate-400 font-bold">Your seats</p>
                  <p class="text-sm font-bold text-slate-700 dark:text-slate-200">
                    {{ Array.isArray(ticket.seats) ? ticket.seats.join(', ') : ticket.seats }}
                  </p>
                </div>
                <div class="text-right">
                  <p class="text-[10px] uppercase tracking-widest text-slate-400 font-bold">Spent</p>
                  <p class="text-lg font-black text-violet-600 dark:text-violet-400">100 pts</p>
                </div>
              </div>
            </div>
  
            <div class="hidden md:flex w-32 bg-slate-50 dark:bg-slate-800/30 items-center justify-center border-l border-dashed border-slate-200 dark:border-slate-700">
              <div class="opacity-20 dark:opacity-40 grayscale group-hover:grayscale-0 transition-all">
                <svg class="w-16 h-16" viewBox="0 0 24 24" fill="currentColor"><path d="M3 3h8v8H3V3zm2 2v4h4V5H5zm8-2h8v8h-8V3zm2 2v4h4V5h-4zM3 13h8v8H3v-8zm2 2v4h4v-4H5zm13-2h3v2h-3v-2zm-3 0h2v2h-2v-2zm3 3h3v2h-3v-2zm-3 0h2v2h-2v-2zm3 3h3v2h-3v-2zm-3 0h2v2h-2v-2z"/></svg>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </template>
  
  