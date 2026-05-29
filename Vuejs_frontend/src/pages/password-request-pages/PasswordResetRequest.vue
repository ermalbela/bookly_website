<template>
  <div>
    <h2 class="text-xl font-semibold text-gray-800 mb-1">Reset your password</h2>
    <p class="text-sm text-gray-400 mb-6">Enter your email and we'll send you a reset link</p>

    <div
      v-if="success"
      class="mb-5 bg-green-50 border border-green-100 text-green-600 text-sm px-4 py-3 rounded-xl"
    >
      Check your email for the reset link
    </div>

    <div
      v-if="error"
      class="mb-5 bg-red-50 border border-red-100 text-red-600 text-sm px-4 py-3 rounded-xl"
    >
      {{ error }}
    </div>

    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-1.5">Email</label>
      <input
        type="email"
        v-model="email"
        placeholder="you@example.com"
        class="w-full px-4 py-2.5 text-sm border border-gray-200 rounded-xl bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all placeholder:text-gray-500"
      />
    </div>

    <button
      type="button"
      :disabled="loading"
      @click="handleRequest"
      class="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-700 disabled:opacity-60 disabled:cursor-not-allowed text-white text-sm font-semibold rounded-xl transition-colors flex items-center justify-center gap-2"
    >
      <i v-if="loading" class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
      {{ loading ? 'Sending…' : 'Send reset link' }}
    </button>

    <p class="text-center text-sm text-gray-400 mt-5">
      Remembered it?
      <RouterLink :to="{ name: 'login' }" class="text-blue-500 font-medium hover:text-blue-700"
        >Sign in</RouterLink
      >
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { authService } from '@/services/auth_service'
import { patterns } from '@/Validation'

const email = ref('')
const loading = ref(false)
const error = ref('')
const success = ref(false)

const handleRequest = async () => {
  error.value = ''
  success.value = false
  loading.value = true
  try {
    if (!patterns.email.test(email.value) || email.value === '') {
      error.value = 'Please provide a valid email'
      return
    }
    await authService.requestPasswordReset(email.value)
    success.value = true
    email.value = ''
  } catch (e: any) {
    error.value = e.response?.data?.detail ?? 'Something went wrong. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
