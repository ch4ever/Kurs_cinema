<template>
  <div class="flex min-h-screen flex-col">
    <AppHeader />
    <div class="mx-auto w-full max-w-3xl flex-1 px-4 py-8 sm:px-6 sm:py-10">
      <div
        class="rounded-2xl border border-slate-300/90 bg-white/90 p-6 shadow-lg shadow-slate-900/10 backdrop-blur dark:border-slate-700/80 dark:bg-slate-900/80 dark:shadow-black/30 sm:p-8"
      >
        <h1 class="text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl dark:text-white">
          Новый фильм
        </h1>
        <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">
          Заполните поля и при необходимости загрузите постер.
        </p>

        <form class="mt-8 space-y-6" @submit.prevent="submitForm">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Название</label>
              <input
                v-model="movieData.title"
                type="text"
                required
                class="mt-1.5 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-slate-900 outline-none transition focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 dark:border-slate-600 dark:bg-slate-800 dark:text-white dark:focus:border-violet-400"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Описание</label>
              <textarea
                v-model="movieData.description"
                rows="3"
                class="mt-1.5 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-slate-900 outline-none transition focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 dark:border-slate-600 dark:bg-slate-800 dark:text-white dark:focus:border-violet-400"
              />
            </div>
          </div>

          <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Дата выхода</label>
              <input
                v-model="movieData.release_date"
                type="date"
                required
                class="mt-1.5 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-slate-900 outline-none transition focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 dark:border-slate-600 dark:bg-slate-800 dark:text-white dark:focus:border-violet-400"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Длительность (мин)</label>
              <input
                v-model="movieData.duration"
                type="number"
                required
                class="mt-1.5 w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-2.5 text-slate-900 outline-none transition focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 dark:border-slate-600 dark:bg-slate-800 dark:text-white dark:focus:border-violet-400"
              />
            </div>
          </div>

          <div>
            <label class="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-300">Постер</label>
            <label
              class="flex h-36 cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed border-slate-300 bg-slate-50/80 transition hover:border-violet-400 hover:bg-violet-50/50 dark:border-slate-600 dark:bg-slate-800/50 dark:hover:border-violet-500 dark:hover:bg-violet-950/20"
            >
              <span class="text-3xl">📸</span>
              <p class="mt-2 px-4 text-center text-sm text-slate-500 dark:text-slate-400">
                <span class="font-semibold text-slate-700 dark:text-slate-200">{{ fileName || 'Нажмите, чтобы выбрать файл' }}</span>
              </p>
              <input type="file" class="hidden" accept="image/*" @change="handleFileUpload" />
            </label>
          </div>

          <div class="flex justify-end border-t border-slate-100 pt-6 dark:border-slate-700">
            <button
              type="submit"
              :disabled="isSubmitting"
              class="inline-flex min-w-[160px] items-center justify-center rounded-xl bg-gradient-to-r from-violet-600 to-fuchsia-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-violet-500/25 transition hover:shadow-xl disabled:cursor-not-allowed disabled:opacity-50"
            >
              {{ isSubmitting ? 'Сохранение…' : 'Создать фильм' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '../api/api'
import { useRouter } from 'vue-router'
import AppHeader from './AppHeader.vue'

const router = useRouter()
const isSubmitting = ref(false)

const movieData = ref({
  title: '',
  description: '',
  release_date: '',
  duration: 120,
})

const posterFile = ref<File | null>(null)
const fileName = ref('')

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return
  posterFile.value = file
  fileName.value = file.name
}

const submitForm = async () => {
  isSubmitting.value = true
  try {
    const formData = new FormData()
    formData.append('title', movieData.value.title)
    formData.append('description', movieData.value.description)
    formData.append('release_date', movieData.value.release_date)
    formData.append('duration', String(movieData.value.duration))
    if (posterFile.value) {
      formData.append('poster', posterFile.value)
    }
    await api.post('movies/', formData)
    alert('Фильм успешно создан!')
    router.push('/')
  } catch (error) {
    console.error(error)
    alert('Ошибка при создании')
  } finally {
    isSubmitting.value = false
  }
}
</script>
