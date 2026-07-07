import { createRouter, createWebHistory } from 'vue-router'
import { userStore } from '@/stores/user'

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
      redirect: '/admin/movies',
    },
    {
      path: '/edit/:id',
      redirect: to => `/admin/movies/${to.params.id}`,
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


    

    {
      path: '/admin',
      component: () => import('@/views/AdminCatalog.vue'),
      meta: { requiresAuth: true, isAdmin: true },
      redirect: '/admin/metrics',
      
      children: [
        {
          path: 'metrics',
          name: 'admin-metrics',
          component: () => import('@/components/admin/Metrics.vue'),
        },
        {
          path: 'movies',
          name: 'admin-movies-create',
          component: () => import('@/views/MovieCreation.vue'),
        },
        {
          path: 'movies/:id',
          name: 'admin-movies-edit',
          component: () => import('@/views/MovieCreation.vue'),
        },
        {
          path: 'actors',
          name: 'admin-actors',
          component: () => import('@/components/admin/Actors.vue'),
        },
        {
          path: 'genres',
          name: 'admin-genres',
          component: () => import('@/components/admin/Genres.vue'),
        },
      ],
    },
  ],
})

router.beforeEach(async (to) => {
  const auth = userStore()

  if (auth.token && !auth.user) {
    await auth.initFromStore()
  }

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return '/'
  }

  if (to.meta.isAdmin && !auth.isAdmin) {
    return '/'
  }
})
