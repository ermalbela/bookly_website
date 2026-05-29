import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth_store'
import AuthLayout from '@/layout/AuthLayout.vue'
import Login from '@/pages/Login.vue'
import Layout from '@/layout/Layout.vue'
import Books from '@/pages/Books.vue'
import NotFound from '@/pages/NotFound.vue'
import BookDetail from '@/pages/BookDetail.vue'
import PasswordResetConfirm from '@/pages/password-request-pages/PasswordResetConfirm.vue'
import PasswordResetRequest from '@/pages/password-request-pages/PasswordResetRequest.vue'
import PasswordResetSuccessfully from '@/pages/password-request-pages/PasswordResetSuccessfully.vue'
import Register from '@/pages/Register.vue'
import Tags from '@/pages/Tags.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/auth',
      component: AuthLayout,
      meta: { requiresGuest: true },
      children: [
        {
          path: 'login',
          name: 'login',
          component: Login,
        },
        {
          path: 'register',
          name: 'register',
          component: Register,
        },
        {
          path: '/password-reset-request',
          name: 'password-reset-request',
          component: PasswordResetRequest
        },
        {
          path: 'password-reset-confirm/:token',
          name: 'password-reset-confirm',
          component: PasswordResetConfirm
        },
        {
          path: 'password-reset-successfully',
          name: 'password-reset-successfully',
          component: PasswordResetSuccessfully
        }
      ],
    },
    {
      path: '/',
      component: Layout,
      meta: { requiresAuth: true },
      children: [
        {
          path: 'books',
          name: 'books',
          component: Books,
        },
        {
          path: 'books/:id',
          name: 'book_detail',
          component: BookDetail,
        },
        {
          path: 'tags',
          name: 'tags',
          component: Tags
        }
      ],
    },

    { path: '/:pathMatch(.*)*', name: 'not_found', component: NotFound },
  ],
})


// ROUTE GUARDS
router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'login' }
  }

  if (to.meta.requiresGuest && auth.isAuthenticated) {
    return { name: 'books' }
  }
})

export default router