<script setup lang="ts">
import { useRouter } from 'vue-router'
import { userStore } from '@/stores/user' 

const props = defineProps<{
  movie: {
    id: number
    title: string
    poster?: string | null
  }
}>()

const router = useRouter()
const auth = userStore()

const goToEdit = () => {
  router.push(`/admin/movies/${props.movie.id}`)
}
</script>

<template>
  <div class="relative aspect-2/3 w-full overflow-hidden rounded-2xl bg-linear-to-br from-slate-200 to-slate-300 shadow-lg ring-1 ring-slate-900/5 transition duration-300 group-hover:shadow-xl group-hover:ring-violet-500/20 dark:from-slate-700 dark:to-slate-800 dark:ring-white/10 dark:group-hover:ring-violet-400/25">
    
    <button
      v-if="auth.isAdmin"
      @click.prevent.stop="goToEdit"
      class="absolute top-3 right-3 z-10 flex h-10 w-10 items-center justify-center rounded-full bg-slate-900/40 text-white backdrop-blur-md transition-all hover:scale-110 hover:bg-violet-600 focus:outline-none focus:ring-2 focus:ring-violet-500 focus:ring-offset-2"
      title="Edit Movie"
    >
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="h-5 w-5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L6.832 19.82a4.5 4.5 0 01-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 011.13-1.897L16.863 4.487zm0 0L19.5 7.125" />
      </svg>
    </button>

    <img
      v-if="movie.poster"
      :src="movie.poster"
      :alt="movie.title"
      class="h-full w-full object-cover transition duration-500 ease-out group-hover:scale-[1.04]"
    />
    
    <div
      v-else
      class="flex h-full w-full items-center justify-center bg-linear-to-br from-violet-100 to-fuchsia-100 dark:from-violet-950/80 dark:to-fuchsia-950/80"
    >
      <span class="select-none text-5xl font-black uppercase text-violet-400/90 dark:text-violet-300/80 sm:text-6xl">
        {{ movie.title.charAt(0) }}
      </span>
    </div>

    <div
      class="pointer-events-none absolute inset-x-0 bottom-0 bg-linear-to-t from-black/85 via-black/45 to-transparent pt-14 pb-3.5 px-3"
    >
      <p class="line-clamp-2 text-center text-sm font-semibold leading-snug text-white drop-shadow-sm sm:text-left">
        {{ movie.title }}
      </p>
    </div>
  </div>
</template>
