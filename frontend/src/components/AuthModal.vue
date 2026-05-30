<script setup lang="ts">
import { ref, watch } from 'vue'
import { userStore } from '@/stores/user'

const auth = userStore()

const username = ref('')
const password = ref('')
const password2 = ref('')
const loading = ref(false)
const errorMsg = ref('')

function resetForm() {
  username.value = ''
  password.value = ''
  password2.value = ''
  errorMsg.value = ''
  loading.value = false
}

watch(
  () => auth.authModalOpen,
  (open) => {
    if (open) resetForm()
  },
)

watch(
  () => auth.authModalTab,
  () => {
    errorMsg.value = ''
  },
)

const passwordsMismatch = () =>
  auth.authModalTab === 'register' &&
  password.value.length > 0 &&
  password2.value.length > 0 &&
  password.value !== password2.value

async function submitLogin() {
  errorMsg.value = ''
  loading.value = true
  try {
    await auth.login(username.value.trim(), password.value)
  } catch (e) {
    errorMsg.value = e instanceof Error ? e.message : 'Ошибка входа'
  } finally {
    loading.value = false
  }
}

async function submitRegister() {
  errorMsg.value = ''
  if (passwordsMismatch()) {
    errorMsg.value = 'Пароли не совпадают'
    return
  }
  loading.value = true
  try {
    await auth.register(username.value.trim(), password.value)
  } catch (e) {
    errorMsg.value = e instanceof Error ? e.message : 'Register Error'
  } finally {
    loading.value = false
  }
}

function onBackdropClick(e: MouseEvent) {
  if ((e.target as HTMLElement).dataset.backdrop === '1') {
    auth.closeAuthModal()
  }
}
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="auth.authModalOpen"
        class="fixed inset-0 z-100 flex items-center justify-center p-4"
        data-backdrop="1"
        @click="onBackdropClick"
      >
        <div class="absolute inset-0 bg-slate-900/60 backdrop-blur-sm dark:bg-black/70" />

        <div
          class="relative z-10 w-full max-w-md overflow-hidden rounded-2xl border border-slate-300/90 bg-slate-50 shadow-2xl shadow-slate-900/20 dark:border-slate-600 dark:bg-slate-900 dark:shadow-black/40"
          role="dialog"
          aria-modal="true"
          aria-labelledby="auth-modal-title"
          @click.stop
        >
          <div class="flex border-b border-slate-200 dark:border-slate-700">
            <button
              type="button"
              class="flex-1 py-3 text-sm font-semibold transition"
              :class="
                auth.authModalTab === 'login'
                  ? 'bg-white text-violet-700 dark:bg-slate-800 dark:text-violet-300'
                  : 'text-slate-500 hover:bg-slate-100/80 dark:text-slate-400 dark:hover:bg-slate-800/50'
              "
              @click="auth.authModalTab = 'login'"
            >
              Login
            </button>
            <button
              type="button"
              class="flex-1 py-3 text-sm font-semibold transition"
              :class="
                auth.authModalTab === 'register'
                  ? 'bg-white text-violet-700 dark:bg-slate-800 dark:text-violet-300'
                  : 'text-slate-500 hover:bg-slate-100/80 dark:text-slate-400 dark:hover:bg-slate-800/50'
              "
              @click="auth.authModalTab = 'register'"
            >
              Register
            </button>
          </div>

          <div class="p-6 sm:p-8">
            <div class="flex items-start justify-between gap-4">
              <h2 id="auth-modal-title" class="text-lg font-bold text-slate-900 dark:text-white">
                {{ auth.authModalTab === 'login' ? 'Login' : 'Account creation' }}
              </h2>
              <button
                type="button"
                class="rounded-lg p-1 text-slate-400 transition hover:bg-slate-200 hover:text-slate-700 dark:hover:bg-slate-700 dark:hover:text-slate-200"
                aria-label="Close"
                @click="auth.closeAuthModal()"
              >
                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <form class="mt-6 space-y-4" @submit.prevent="auth.authModalTab === 'login' ? submitLogin() : submitRegister()">
              <div
                v-if="errorMsg"
                class="rounded-xl border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800 dark:border-red-900/40 dark:bg-red-950/50 dark:text-red-200"
              >
                {{ errorMsg }}
              </div>

              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Login</label>
                <input
                  v-model="username"
                  type="text"
                  autocomplete="username"
                  required
                  minlength="3"
                  class="mt-1.5 w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 outline-none transition focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 dark:border-slate-600 dark:bg-slate-800 dark:text-white"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Password</label>
                <input
                  v-model="password"
                  type="password"
                  :autocomplete="auth.authModalTab === 'login' ? 'current-password' : 'new-password'"
                  required
                  minlength="3"
                  class="mt-1.5 w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 outline-none transition focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 dark:border-slate-600 dark:bg-slate-800 dark:text-white"
                />
              </div>
              <div v-if="auth.authModalTab === 'register'">
                <label class="block text-sm font-medium text-slate-700 dark:text-slate-300">Repeat password</label>
                <input
                  v-model="password2"
                  type="password"
                  autocomplete="new-password"
                  required
                  class="mt-1.5 w-full rounded-xl border border-slate-300 bg-white px-4 py-2.5 text-slate-900 outline-none transition focus:border-violet-500 focus:ring-2 focus:ring-violet-500/20 dark:border-slate-600 dark:bg-slate-800 dark:text-white"
                />
                <p v-if="passwordsMismatch()" class="mt-1 text-xs text-amber-700 dark:text-amber-400">
                  Passwords needs to match
                </p>
              </div>

              <button
                type="submit"
                :disabled="loading || passwordsMismatch()"
                class="w-full rounded-xl bg-linear-to-r from-violet-600 to-fuchsia-600 py-3 text-sm font-semibold text-white shadow-md shadow-violet-500/20 transition hover:shadow-lg disabled:opacity-50"
              >
                {{ loading ? 'wait…' : auth.authModalTab === 'login' ? 'Login' : 'Register' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
