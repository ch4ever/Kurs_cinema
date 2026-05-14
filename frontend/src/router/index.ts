import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/components/HomeView.vue'),
    },
    {
      path: '/create',
      name: 'create',
      component: () => import('@/components/MovieCreation.vue'),
    },
    {
      path: '/booking/:id',
      name: 'booking',
      component: () => import('@/components/MovieBooking.vue'),
    },
    { path: '/login', redirect: '/' },
    { path: '/register', redirect: '/' },
  ],
})

export default router
