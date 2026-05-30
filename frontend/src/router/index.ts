import { createRouter, createWebHistory } from 'vue-router'

export const router = createRouter({
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
      component: () => import('@/views/MovieCreation.vue'),
    },
    {
      path: '/edit/:id',
      name: 'edit',
      component: () => import('@/views/MovieCreation.vue') 
    },
    {
      path: '/booking/:id',
      name: 'booking',
      component: () => import('@/views/MovieBooking.vue'),
    },
    {
      path: '/movie/:id',
      name: 'movie detail',
      component: () =>import('@/views/MovieDetail.vue')
    },
    {
      path: '/profile/tickets',
      name: 'my-tickets',
      component: () => import('@/components/UserTickets.vue'),
      meta: { requiresAuth: true }
    },
    { path: '/login', redirect: '/' },
    { path: '/register', redirect: '/' },
  ],
})

// export default router
