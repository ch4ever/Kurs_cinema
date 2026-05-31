<script setup lang="ts">
//   (ActorsStore)
  </script>
<!-- src/views/admin/Actors.vue -->
<template>
    <div class="max-w-3xl space-y-6">
  
      <div class="mb-6 border-b border-slate-200 dark:border-slate-800 pb-4">
        <h1 class="text-3xl font-bold text-slate-900 dark:text-white">
          Actors
        </h1>
        <p class="text-slate-500 dark:text-slate-400 mt-2">
          Actor creation and control
        </p>
      </div>
  
      <!-- CREATE FORM -->
      <div class="rounded-2xl p-5 bg-white dark:bg-[#0f1423] ring-1 ring-slate-900/5 dark:ring-white/10">
        
        <h2 class="text-lg font-semibold text-slate-900 dark:text-white mb-4">
          Add Actor
        </h2>
  <!-- TODO ADD POSTER -->
        <form class="space-y-4">
          <input
            type="text"
            placeholder="Name"
            class="w-full px-4 py-3 rounded-xl bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700"
          />
  
          <input
            type="text"
            placeholder="Surname"
            class="w-full px-4 py-3 rounded-xl bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700"
          />
  
          <input
            type="text-area"
            class="w-full px-4 py-3 rounded-xl bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700"
          />
  
          <button
            type="submit"
            class="px-6 py-2 rounded-xl bg-violet-600 text-white"
          >
            Create
          </button>
        </form>
      </div>
  
    </div>
  </template>
  