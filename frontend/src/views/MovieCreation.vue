<script setup lang="ts">
  import { ref, onMounted, computed, watch } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import { useMovieStore } from '@/stores/Movie';
  import { useAlertStore } from '@/stores/alerts';
  
  const route = useRoute();
  const router = useRouter();
  const movieStore = useMovieStore();
  const alerts = useAlertStore();
  
  const isSubmitting = ref(false);
  
  
  const movieId = computed(() => route.params.id);
  const isEditing = computed(() => !!movieId.value);
  
  const movieData = ref({
    title: '',
    description: '',
    release_date: '',
  });
  
  const posterFile = ref<File | null>(null);
  const fileName = ref('');
  const existingPoster = ref('');
  
  const resetForm = () => {
    movieData.value = {
      title: '',
      description: '',
      release_date: '',
    };
    posterFile.value = null;
    fileName.value = '';
    existingPoster.value = '';
  };
  
  const loadMovieData = async () => {
    if (isEditing.value) {
      
      await movieStore.getMovie(Number(movieId.value));
      
      
      if (movieStore.movie) {
        movieData.value = {
          title: movieStore.movie.title,
          description: movieStore.movie.description,
          release_date: movieStore.movie.release_date,
        };
        existingPoster.value = movieStore.movie.poster || '';
      }
    } else {
      resetForm();
    }
  };

  onMounted(async () => {
    await loadMovieData();
  });

  watch(movieId, async () => {
    await loadMovieData();
  });
  
  const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const files = target.files;
  const selectedFile = files?.item(0);
  if (selectedFile) {
    posterFile.value = selectedFile;
    fileName.value = selectedFile.name;
  } else {
    posterFile.value = null;
    fileName.value = '';
  }
};
 
  
  const submitForm = async () => {
    isSubmitting.value = true;
    try {
      const formData = new FormData();
      formData.append('title', movieData.value.title);
      formData.append('description', movieData.value.description);
      formData.append('release_date', movieData.value.release_date);
      
      if (posterFile.value) {
        formData.append('poster', posterFile.value);
      }
      if (isEditing.value) {
        await movieStore.updateMovie(Number(movieId.value), formData);
        alerts.showSuccessAlert("Film updated successfully")
        router.push(`/movie/${movieId.value}`);
      } 
      else {
        const newMovie = await movieStore.createMovie(formData);
        alerts.showSuccessAlert("Film created successfully")
        const newMovieId = newMovie.id;
        router.push(`/movie/${newMovieId}`);
      }
  
       
    } catch (error) {
        console.log(error)
      
    } finally {
      isSubmitting.value = false;
    }
  };
  </script>

<template>
    <div class="max-w-3xl mx-auto p-6 bg-white dark:bg-[#0f1423] rounded-3xl shadow-xl ring-1 ring-slate-900/5 dark:ring-white/10 mt-10 mb-20 transition-colors duration-300">
      <div class="mb-8 border-b border-slate-200 dark:border-slate-800 pb-4">
        <h1 class="text-3xl font-bold text-slate-900 dark:text-white flex items-center gap-3">
          <span class="text-4xl">{{ isEditing ? '✏️' : '🎬' }}</span>
          {{ isEditing ? 'Редактировать фильм' : 'Добавить новый фильм' }}
        </h1>
        <p class="text-slate-500 dark:text-slate-400 mt-2">
          {{ isEditing ? 'Внесите изменения в данные фильма.' : 'Заполните информацию о новом фильме для проката.' }}
        </p>
      </div>
      
      <form @submit.prevent="submitForm" class="space-y-6">
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-1.5">Название фильма *</label>
            <input v-model="movieData.title" type="text" required placeholder="Например: Дюна: Часть вторая" class="w-full px-4 py-3 bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white focus:ring-2 focus:ring-violet-500 focus:border-violet-500 outline-none transition-all" />
          </div>
          <div>
            <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-1.5">Описание *</label>
            <textarea v-model="movieData.description" rows="4" required placeholder="Краткий синопсис..." class="w-full px-4 py-3 bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white focus:ring-2 focus:ring-violet-500 focus:border-violet-500 outline-none transition-all resize-y"></textarea>
          </div>
        </div>
  
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-1.5">Дата выхода *</label>
            <input v-model="movieData.release_date" type="date" required class="w-full px-4 py-3 bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-900 dark:text-white focus:ring-2 focus:ring-violet-500 outline-none transition-all" />
          </div>
          </div>
  
        <div>
          <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">Постер фильма</label>
          
          <div v-if="isEditing && existingPoster" class="mb-4 flex items-start gap-4 p-4 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700">
            <img :src="existingPoster" alt="Current poster" class="h-24 w-16 object-cover rounded shadow-sm">
            <div>
              <p class="text-sm font-medium text-slate-700 dark:text-slate-300">Текущий постер</p>
              <p class="text-xs text-slate-500 mt-1">Загрузите новый файл ниже, если хотите его заменить.</p>
            </div>
          </div>
  
          <div class="flex items-center justify-center w-full">
            <label class="group flex flex-col items-center justify-center w-full h-36 border-2 border-dashed border-slate-300 dark:border-slate-600 rounded-2xl cursor-pointer bg-slate-50/50 dark:bg-slate-900/30 hover:bg-violet-50 dark:hover:bg-violet-900/10 hover:border-violet-400 dark:hover:border-violet-500 transition-all duration-200">
              <div class="flex flex-col items-center justify-center pt-5 pb-6">
                <span class="text-3xl mb-2 transition-transform group-hover:scale-110">📸</span>
                <p class="text-sm text-slate-500 dark:text-slate-400 text-center px-4">
                  <span class="font-semibold text-violet-600 dark:text-violet-400">
                    {{ fileName || (isEditing ? 'Нажмите, чтобы заменить картинку' : 'Нажмите, чтобы загрузить картинку') }}
                  </span>
                </p>
              </div>
              <input type="file" class="hidden" @change="handleFileUpload" accept="image/*" />
            </label>
          </div>
        </div>
  
        <div class="flex justify-end gap-3 pt-6 border-t border-slate-200 dark:border-slate-800">
          <button 
            type="button" 
            @click="$router.push('/')" 
            class="px-6 py-3 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 font-medium transition-colors"
          >
            Отмена
          </button>
          <button 
            type="submit" 
            :disabled="isSubmitting" 
            class="px-8 py-3 bg-violet-600 text-white font-semibold rounded-xl hover:bg-violet-500 focus:ring-4 focus:ring-violet-500/20 transition-all shadow-md shadow-violet-500/20 disabled:opacity-70 disabled:cursor-not-allowed"
          >
            {{ isSubmitting ? 'Сохранение...' : (isEditing ? 'Сохранить изменения' : 'Создать фильм') }}
          </button>
        </div>
  
      </form>
    </div>
  </template>
  
  
