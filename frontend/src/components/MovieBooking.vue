<template>
  <div class="flex min-h-screen flex-col">
    <AppHeader />
    <div class="mx-auto w-full max-w-4xl flex-1 px-4 py-8 sm:px-6 sm:py-10">
      <div
        class="rounded-2xl border border-slate-300/90 bg-white/90 p-6 shadow-lg shadow-slate-900/10 backdrop-blur dark:border-slate-700/80 dark:bg-slate-900/80 dark:shadow-black/30 sm:p-10"
      >
        <h2 class="text-center text-2xl font-extrabold tracking-tight text-slate-900 sm:text-3xl dark:text-white">
          Выберите места
        </h2>
        <p class="mt-2 text-center text-sm text-slate-500 dark:text-slate-400">
          Билет: <span class="font-semibold text-violet-600 dark:text-violet-400">{{ ticketPrice }} ₽</span>
        </p>

        <div class="relative mx-auto mb-12 mt-10 h-12 w-3/4 max-w-xl">
          <div class="absolute inset-0 rounded-[100%] bg-violet-500/15 blur-2xl dark:bg-violet-500/25" />
          <div
            class="relative flex h-8 w-full items-start justify-center rounded-t-[50%] border-t-4 border-violet-500 pt-2 text-xs font-bold uppercase tracking-[0.2em] text-violet-600 dark:text-violet-400"
          >
            Экран
          </div>
        </div>

        <div class="mb-10 flex flex-col items-center gap-4">
          <div v-for="row in rows" :key="row" class="flex items-center gap-3 sm:gap-4">
            <span class="w-5 text-center text-xs font-bold text-slate-400 sm:w-6 sm:text-sm">{{ row }}</span>
            <div class="flex gap-1.5 sm:gap-2">
              <button
                v-for="col in cols"
                :key="col"
                type="button"
                :disabled="isBooked(row, col)"
                :class="[
                  'h-8 w-8 rounded-t-lg transition sm:h-10 sm:w-10',
                  isBooked(row, col)
                    ? 'cursor-not-allowed bg-slate-700 opacity-45 dark:bg-slate-600'
                    : isSelected(row, col)
                      ? 'scale-110 bg-gradient-to-b from-violet-600 to-fuchsia-600 shadow-lg shadow-violet-500/40'
                      : 'cursor-pointer bg-slate-200 hover:bg-violet-300 dark:bg-slate-600 dark:hover:bg-violet-500/70',
                ]"
                @click="toggleSeat(row, col)"
              />
            </div>
            <span class="w-5 text-center text-xs font-bold text-slate-400 sm:w-6 sm:text-sm">{{ row }}</span>
          </div>
        </div>

        <div
          class="mb-8 flex flex-wrap justify-center gap-6 text-xs font-medium text-slate-600 sm:text-sm dark:text-slate-300"
        >
          <div class="flex items-center gap-2">
            <div class="h-5 w-5 rounded-t bg-slate-200 dark:bg-slate-600" />
            Свободно
          </div>
          <div class="flex items-center gap-2">
            <div class="h-5 w-5 rounded-t bg-gradient-to-b from-violet-600 to-fuchsia-600" />
            Выбрано
          </div>
          <div class="flex items-center gap-2">
            <div class="h-5 w-5 rounded-t bg-slate-700 opacity-50 dark:bg-slate-500" />
            Занято
          </div>
        </div>

        <div
          class="flex flex-col items-center justify-between gap-4 border-t border-slate-100 pt-6 dark:border-slate-700 sm:flex-row sm:items-end"
        >
          <div class="text-center sm:text-left">
            <p class="text-sm text-slate-500 dark:text-slate-400">
              Билетов:
              <span class="font-bold text-slate-900 dark:text-white">{{ selectedSeats.length }}</span>
            </p>
            <p class="text-xl font-bold text-slate-900 dark:text-white">
              К оплате: {{ totalPrice }} ₽
            </p>
          </div>
          <button
            type="button"
            :disabled="selectedSeats.length === 0 || isLoading"
            class="w-full rounded-xl bg-gradient-to-r from-violet-600 to-fuchsia-600 px-8 py-3 text-sm font-bold text-white shadow-lg shadow-violet-500/25 transition hover:shadow-xl disabled:cursor-not-allowed disabled:opacity-45 sm:w-auto"
            @click="buyTickets"
          >
            {{ isLoading ? 'Оформление…' : 'Купить билеты' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api/api'
import AppHeader from './AppHeader.vue'

const route = useRoute()
const router = useRouter()
const movieId = String(route.params.id ?? '')

const ticketPrice = 450
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
    alert('Билеты успешно куплены! 🎉')
    router.push('/')
  } catch (error) {
    alert('Ошибка при покупке. Возможно, места уже заняты.')
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
    console.error('Не удалось загрузить занятые места', e)
    bookedSeats.value = []
  }
}

onMounted(() => {
  void loadBookedSeats()
})
</script>
