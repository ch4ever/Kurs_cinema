<script setup lang="ts">
defineProps<{
  movie: {
    id: number
    title: string
    poster?: string | null
  }
}>()
</script>

<template>
  <div
    class="relative aspect-[2/3] w-full overflow-hidden rounded-2xl bg-gradient-to-br from-slate-200 to-slate-300 shadow-lg ring-1 ring-slate-900/5 transition duration-300 group-hover:shadow-xl group-hover:ring-violet-500/20 dark:from-slate-700 dark:to-slate-800 dark:ring-white/10 dark:group-hover:ring-violet-400/25"
  >
    <img
      v-if="movie.poster"
      :src="movie.poster"
      :alt="movie.title"
      class="h-full w-full object-cover transition duration-500 ease-out group-hover:scale-[1.04]"
    />
    <div
      v-else
      class="flex h-full w-full items-center justify-center bg-gradient-to-br from-violet-100 to-fuchsia-100 dark:from-violet-950/80 dark:to-fuchsia-950/80"
    >
      <span class="select-none text-5xl font-black uppercase text-violet-400/90 dark:text-violet-300/80 sm:text-6xl">
        {{ movie.title.charAt(0) }}
      </span>
    </div>

    <div
      class="pointer-events-none absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/85 via-black/45 to-transparent pt-14 pb-3.5 px-3"
    >
      <p class="line-clamp-2 text-center text-sm font-semibold leading-snug text-white drop-shadow-sm sm:text-left">
        {{ movie.title }}
      </p>
    </div>
  </div>
</template>
