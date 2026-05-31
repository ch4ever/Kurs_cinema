<!-- AdminLayout.vue -->
<template>
    <div class="min-h-screen flex bg-slate-100 dark:bg-[#0b0f1a]">
  
      <!-- SIDEBAR -->
      <aside class="w-72 border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-[#0f1423] p-4">
  
        <h2 class="text-xl font-bold text-slate-900 dark:text-white mb-6">
          Admin Panel
        </h2>
  
        <nav class="space-y-2">
  
          <RouterLink
            to="/admin/metrics"
            class="block px-4 py-3 rounded-xl transition"
            active-class="bg-violet-600 text-white shadow-md"
          >
            <div class="font-semibold">Metrics</div>
            <div class="text-xs opacity-70">Statistics</div>
          </RouterLink>
  
          <RouterLink
            to="/admin/movies"
            class="block px-4 py-3 rounded-xl transition"
            active-class="bg-violet-600 text-white shadow-md"
          >
            <div class="font-semibold">Films</div>
            <div class="text-xs opacity-70">Creation/redaction</div>
          </RouterLink>
  
          <RouterLink
            to="/admin/actors"
            class="block px-4 py-3 rounded-xl transition"
            active-class="bg-violet-600 text-white shadow-md"
          >
            <div class="font-semibold">Actors</div>
          </RouterLink>
  
          <RouterLink
            to="/admin/genres"
            class="block px-4 py-3 rounded-xl transition"
            active-class="bg-violet-600 text-white shadow-md"
          >
            <div class="font-semibold">Genres</div>
          </RouterLink>
  
        </nav>
      </aside>
  
      <!-- CONTENT -->
      <main class="flex-1 p-8">
        <RouterView />
      </main>
  
    </div>
  </template>