<template>
  <div class="min-h-screen bg-slate-50 dark:bg-[#0B0F19] transition-colors duration-300">
    <AppHeader />

    <main class="mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
      <div v-if="movieStore.movie" class="mb-12 flex flex-col items-center gap-4 text-center">
        <h1 class="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">
          {{ movieStore.movie.title }}
        </h1>
        <div class="flex items-center gap-3 text-sm font-medium text-slate-500 dark:text-slate-400">
          <span class="px-2 py-0.5 rounded border border-slate-200 dark:border-slate-800">2D</span>
          <span>•</span>
          <span>Hall 1</span>
          <span>•</span>
          <span class="text-violet-600 dark:text-violet-400 font-bold">{{ ticketPrice }} points / seat</span>
        </div>
      </div>

      <div class="relative overflow-hidden rounded-[2.5rem] bg-white/70 dark:bg-slate-900/40 p-8 shadow-2xl ring-1 ring-slate-200/50 backdrop-blur-xl dark:ring-white/5 sm:p-12">
        
        <div class="relative mx-auto mb-20 w-4/5 max-w-2xl">
          <div class="absolute -top-10 left-1/2 h-20 w-full -translate-x-1/2 bg-violet-500/20 blur-[60px] dark:bg-violet-500/10" />
          
          <div class="relative overflow-hidden">
            <div class="h-1.5 w-full rounded-full bg-gradient-to-r from-transparent via-violet-500 to-transparent shadow-[0_0_20px_rgba(139,92,246,0.5)]" />
            <p class="mt-4 text-center text-[10px] font-black uppercase tracking-[0.4em] text-slate-400 dark:text-slate-500">
              Cinema Screen
            </p>
          </div>
        </div>

        <div class="mb-16 flex flex-col items-center gap-6 overflow-x-auto pb-4">
          <div v-for="row in rows" :key="row" class="flex items-center gap-4">
            <span class="w-6 text-right text-[10px] font-black text-slate-400">{{ row }}</span>
            
            <div class="flex gap-2 sm:gap-3">
              <button
                v-for="col in cols"
                :key="col"
                type="button"
                :disabled="isBooked(row, col)"
                :class="[
                  'group relative h-8 w-8 rounded-lg transition-all duration-300 sm:h-10 sm:w-10',
                  isBooked(row, col)
                    ? 'cursor-not-allowed bg-slate-200 dark:bg-slate-800'
                    : isSelected(row, col)
                      ? 'scale-110 bg-gradient-to-br from-violet-500 to-fuchsia-500 shadow-xl shadow-violet-500/40'
                      : 'bg-white border border-slate-200 hover:border-violet-400 hover:shadow-md dark:bg-slate-800/50 dark:border-slate-700 dark:hover:border-violet-500'
                ]"
                @click="toggleSeat(row, col)"
              >
                <div 
                  v-if="!isBooked(row, col)"
                  :class="[
                    'absolute inset-x-1.5 bottom-1 h-1 rounded-full transition-colors',
                    isSelected(row, col) ? 'bg-white/40' : 'bg-slate-200 dark:bg-slate-700 group-hover:bg-violet-300'
                  ]" 
                />
                
                <span v-if="isBooked(row, col)" class="text-[8px] opacity-20 dark:opacity-40 font-bold">X</span>
              </button>
            </div>

            <span class="w-6 text-left text-[10px] font-black text-slate-400">{{ row }}</span>
          </div>
        </div>

        <div class="flex flex-wrap justify-center gap-8 border-t border-slate-100 py-8 dark:border-slate-800">
          <div class="flex items-center gap-3 text-xs font-bold text-slate-500">
            <div class="h-4 w-4 rounded bg-white border border-slate-200 dark:bg-slate-800 dark:border-slate-700" />
            Available
          </div>
          <div class="flex items-center gap-3 text-xs font-bold text-slate-500">
            <div class="h-4 w-4 rounded bg-gradient-to-br from-violet-500 to-fuchsia-500" />
            Selected
          </div>
          <div class="flex items-center gap-3 text-xs font-bold text-slate-500">
            <div class="h-4 w-4 rounded bg-slate-200 dark:bg-slate-800" />
            Occupied
          </div>
        </div>

        <div class="flex flex-col items-center justify-between gap-6 sm:flex-row">
          <div class="flex flex-col gap-1 text-center sm:text-left">
            <p class="text-xs font-bold uppercase tracking-widest text-slate-400">Total Selection</p>
            <div class="flex items-baseline gap-2">
              <span class="text-3xl font-black text-slate-900 dark:text-white">{{ totalPrice }}</span>
              <span class="text-sm font-bold text-slate-500">points</span>
            </div>
            <p v-if="selectedSeats.length > 0" class="text-[10px] text-violet-600 dark:text-violet-400 font-bold uppercase">
              {{ selectedSeats.length }} seats: {{ selectedSeats.join(', ') }}
            </p>
          </div>

          <button
            type="button"
            :disabled="selectedSeats.length === 0 || isLoading"
            @click="buyTickets"
            class="group relative w-full sm:w-auto overflow-hidden rounded-2xl bg-slate-900 px-12 py-4 text-sm font-black text-white transition-all hover:scale-[1.02] active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-50 dark:bg-violet-600"
          >
            <div class="absolute inset-0 bg-gradient-to-r from-violet-400 to-fuchsia-400 opacity-0 transition-opacity group-hover:opacity-10" />
            <span class="relative flex items-center justify-center gap-2">
              {{ isLoading ? 'Processing...' : 'Complete Booking' }}
              <span v-if="!isLoading" class="text-lg">→</span>
            </span>
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api/api'
import AppHeader from './AppHeader.vue'
import { useMovieStore } from '@/stores/Movie'

const route = useRoute()
const router = useRouter()
const movieStore = useMovieStore()
const movieId = String(route.params.id ?? '')

const ticketPrice = 100
const isLoading = ref(false)

const rows = ['A', 'B', 'C', 'D', 'E', 'F']
const cols = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

const bookedSeats = ref<string[]>([])
const selectedSeats = ref<string[]>([])

const totalPrice = computed(() => selectedSeats.value.length * ticketPrice)

const isBooked = (row: string, col: number) => bookedSeats.value.includes(`${row}${col}`)
const isSelected = (row: string, col: number) => selectedSeats.value.includes(`${row}${col}`)

const toggleSeat = (row: string, col: number) => {
  const seatId = `${row}${col}`
  if (isBooked(row, col)) return
  if (isSelected(row, col)) {
    selectedSeats.value = selectedSeats.value.filter((s) => s !== seatId)
  } else {
    selectedSeats.value.push(seatId)
  }
}

const buyTickets = async () => {
  isLoading.value = true
  try {
    await api.post(`movies/${movieId}/book/`, {
      seats: selectedSeats.value,
    })
    alert('Tickets purchased successfully! 🎉')
    router.push('/')
  } catch (error) {
    alert('Error while purchasing tickets.')
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

async function loadBookedSeats() {
  if (!movieId) return
  try {
    const { data } = await api.get<{ booked_seats: string[] }>(`movies/${movieId}/seats/`)
    bookedSeats.value = Array.isArray(data.booked_seats) ? data.booked_seats : []
  } catch (e) {
    console.error('Error loading booked seats', e)
    bookedSeats.value = []
  }
}

onMounted(() => {
  void loadBookedSeats()
  // Also load movie info if not present in store
  if (movieId) {
    void movieStore.getMovie(Number(movieId))
  }
})
</script>

<style scoped>
/* Custom scrollbar for seats on mobile */
::-webkit-scrollbar {
  height: 4px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: rgba(139, 92, 246, 0.2);
  border-radius: 10px;
}
</style>