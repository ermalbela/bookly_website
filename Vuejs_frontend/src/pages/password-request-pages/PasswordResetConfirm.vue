<template>
  <div>
    <h2 class="text-xl font-semibold text-gray-800 mb-1">Set new password</h2>
    <p class="text-sm text-gray-400 mb-6">Choose a strong password for your account</p>

    <div v-if="success" class="mb-5 bg-green-50 border border-green-100 text-green-600 text-sm px-4 py-3 rounded-xl">
      Password reset! <RouterLink :to="{ name: 'login' }" class="font-medium underline">Sign in</RouterLink>
    </div>

    <div v-if="error" class="mb-5 bg-red-50 border border-red-100 text-red-600 text-sm px-4 py-3 rounded-xl">
      {{ error }}
    </div>

    <div class="mb-4">
      <label class="block text-sm font-medium text-gray-700 mb-1.5">New password</label>
      <input
        type="password"
        v-model="form.new_password"
        placeholder="••••••••"
        class="w-full px-4 py-2.5 text-sm border border-gray-200 rounded-xl bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all placeholder:text-gray-500"
      />
    </div>

    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-1.5">Confirm password</label>
      <input
        type="password"
        v-model="form.confirm_new_password"
        placeholder="••••••••"
        class="w-full px-4 py-2.5 text-sm border border-gray-200 rounded-xl bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all placeholder:text-gray-500"
      />
    </div>

    <button
      type="button"
      :disabled="loading"
      @click="handleConfirm"
      class="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-700 disabled:opacity-60 disabled:cursor-not-allowed text-white text-sm font-semibold rounded-xl transition-colors flex items-center justify-center gap-2"
    >
      <i v-if="loading" class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
      {{ loading ? 'Resetting…' : 'Reset password' }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { authService } from '@/services/auth_service'

const route = useRoute()
const router = useRouter()

const form = ref({ new_password: '', confirm_new_password: '' })
const loading = ref(false)
const error = ref('')
const success = ref(false)

const handleConfirm = async () => {
  error.value = ''
  loading.value = true
  try {
    await authService.confirmPasswordReset(route.params.token as string, form.value.new_password, form.value.confirm_new_password)
    success.value = true
    router.push({ name: 'password-reset-successfully' })
  } catch (e: any) {
    error.value = e.response?.data?.detail ?? 'Reset failed. The link may have expired.'
  } finally {
    loading.value = false
  }
}
</script>