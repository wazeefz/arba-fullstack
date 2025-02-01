// router/index.ts
import { createRouter, createWebHistory } from 'vue-router/auto'
import { setupLayouts } from 'virtual:generated-layouts'
import { routes } from 'vue-router/auto-routes'

// Add a redirect to /login for the root path

const redirectRoutes = [
  {
    path: '/',
    redirect: '/login', // Redirect root to login
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    ...redirectRoutes, // Add the redirect route here
    ...setupLayouts(routes), // Use the automatically generated routes
  ],
})

router.beforeEach((to, from) => {
  console.log('Navigating to:', to)

  if (to.meta.requiresAuth) {
    const isAuthenticated = localStorage.getItem('token')
    console.log('Authenticated:', isAuthenticated)

    if (!isAuthenticated) {
      console.log('Redirecting to login')
      return {
        path: '/login', // Redirect to login if not authenticated
        query: { returnTo: from.fullPath },
      }
    }
  }
})

// Workaround for https://github.com/vitejs/vite/issues/11804
router.onError((err, to) => {
  if (err?.message?.includes?.('Failed to fetch dynamically imported module')) {
    if (!localStorage.getItem('vuetify:dynamic-reload')) {
      console.log('Reloading page to fix dynamic import error')
      localStorage.setItem('vuetify:dynamic-reload', 'true')
      location.assign(to.fullPath)
    } else {
      console.error('Dynamic import error, reloading page did not fix it', err)
    }
  } else {
    console.error(err)
  }
})

router.isReady().then(() => {
  localStorage.removeItem('vuetify:dynamic-reload')
})

export default router
