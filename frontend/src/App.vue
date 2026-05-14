<script setup lang="ts">
import { useUserSettingsStore } from './stores/userSettings'
import { onMounted } from 'vue'
import AuthModal from './components/AuthModal.vue'

const userSettingsStore = useUserSettingsStore()

onMounted(() => {
  userSettingsStore.initTheme()
})
</script>

<template>
  <div
    class="min-h-screen w-full bg-gradient-to-b from-slate-200 via-slate-100 to-slate-200 text-slate-800 dark:from-slate-950 dark:via-slate-950 dark:to-slate-900 dark:text-slate-100"
  >
    <router-view />
    <AuthModal />
  </div>
</template>
