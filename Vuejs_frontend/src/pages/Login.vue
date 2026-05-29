<template>
  <div class="flex items-center justify-center px-4">
    <div class="w-full max-w-sm">
      <div class="text-center mb-8">
        <span class="text-3xl font-black tracking-widest text-blue-600">BOOKLY</span>
        <h2 class="text-xl font-semibold text-gray-800 mt-3">Welcome back</h2>
        <p class="text-sm text-gray-400 mt-1">Sign in to your Bookly account</p>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
        <div
          v-if="error"
          class="mb-5 flex items-start gap-2.5 bg-red-50 border border-red-100 text-red-600 text-sm px-4 py-3 rounded-xl"
        >
          <i class="pi pi-exclamation-circle" style="font-size: 1rem"></i>
          {{ error }}
        </div>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1.5">Email</label>
          <input
            type="email"
            v-model="form.email"
            placeholder="you@example.com"
            class="w-full px-4 py-2.5 text-sm border border-gray-200 rounded-xl bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all placeholder:text-gray-500"
          />
        </div>
        <div class="mb-6">
          <label class="text-sm font-medium text-gray-700">Password</label>
          <input
            type="password"
            v-model="form.password"
            placeholder="••••••••"
            class="w-full px-4 py-2.5 text-sm border border-gray-200 rounded-xl bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all placeholder:text-gray-500"
          />
          <div class="flex justify-end mt-2">
            <RouterLink
              :to="{ name: 'password-reset-request' }"
              class="text-xs text-blue-500 hover:text-blue-700"
              >Forgot password?</RouterLink
            >
          </div>
        </div>

        <button
          type="button"
          :disabled="loading"
          @click="handleLogin"
          class="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-700 active:bg-blue-800 disabled:opacity-60 disabled:cursor-not-allowed text-white text-sm font-semibold rounded-xl transition-colors duration-150 flex items-center justify-center gap-2"
        >
          <i v-if="loading" class="pi pi-spin pi-spinner" style="font-size: 1.3rem"></i>
          {{ loading ? 'Signing in…' : 'Sign in' }}
        </button>

        <p class="text-center text-sm text-gray-500 mt-5">
          Don't have an account?
          <RouterLink :to="{ name: 'register' }" class="text-blue-500 font-medium hover:text-blue-700">Register</RouterLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth_store'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({ email: '', password: '' })
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  error.value = ''
  loading.value = true
  try {
    await authStore.login(form.value.email, form.value.password)
    router.push({ name: 'books' })
  } catch (e: any) {
    error.value = e.response?.data?.detail ?? 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
