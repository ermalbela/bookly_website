<template>
  <div class="flex items-center justify-center px-4">
    <div class="w-full max-w-xl">
      <div class="text-center mb-8">
        <span class="text-3xl font-black tracking-widest text-blue-600">BOOKLY</span>
        <h2 class="text-xl font-semibold text-gray-800 mt-3">Welcome back</h2>
        <p class="text-sm text-gray-400 mt-1">Sign in to your Bookly account</p>
      </div>

      <div class="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
        <div
          v-if="error"
          class="mb-5 flex items-start gap-2.5 bg-red-50 border border-red-100 
          text-red-600 text-sm px-4 py-3 rounded-xl"
        >
          <i class="pi pi-exclamation-circle" style="font-size: 1rem"></i>
          {{ error }}
        </div>

        <div
          v-if="success"
          class="mb-5 flex items-start gap-2.5 bg-green-50 border border-green-100 
          text-green-600 text-sm px-4 py-3 rounded-xl"
        >
          <i class="pi pi-exclamation-circle" style="font-size: 1rem"></i>
          {{ success }}
        </div>

        <div class="mb-4 flex md:flex-row flex-col justify-between">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">First Name</label>
            <input
              type="text"
              v-model="form.first_name"
              placeholder="John"
              class="w-full px-4 py-2.5 text-sm border border-gray-200 rounded-xl 
              bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent 
              transition-all placeholder:text-gray-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Last Name</label>
            <input
              type="text"
              v-model="form.last_name"
              placeholder="Doe"
              class="w-full px-4 py-2.5 text-sm border border-gray-200 rounded-xl 
              bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent 
              transition-all placeholder:text-gray-500"
            />
          </div>
        </div>
        <div class="mb-4 flex md:flex-row flex-col justify-between">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Username</label>
            <input
              type="text"
              v-model="form.username"
              placeholder="JohnDoe"
              class="w-full px-4 py-2.5 text-sm border border-gray-200 rounded-xl 
              bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent 
              transition-all placeholder:text-gray-500"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5">Email</label>
            <input
              type="email"
              v-model="form.email"
              placeholder="doe@gmail.com"
              class="w-full px-4 py-2.5 text-sm border border-gray-200 rounded-xl 
              bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent 
              transition-all placeholder:text-gray-500"
            />
          </div>
        </div>
        <div class="mb-6">
          <label class="text-sm font-medium text-gray-700">Password</label>
          <input
            type="password"
            v-model="form.password"
            placeholder="••••••••"
            class="w-full px-4 py-2.5 text-sm border border-gray-200 rounded-xl 
            bg-gray-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent 
            transition-all placeholder:text-gray-500"
          />
        </div>

        <button
          type="button"
          :disabled="loading"
          @click="handleRegister"
          class="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-700 active:bg-blue-800 
          disabled:opacity-60 disabled:cursor-not-allowed text-white text-sm font-semibold rounded-xl 
          transition-colors duration-150 flex items-center justify-center gap-2"
        >
          <i v-if="loading" class="pi pi-spin pi-spinner" style="font-size: 1.3rem"></i>
          {{ loading ? 'Signing in…' : 'Sign in' }}
        </button>

        <p class="text-center text-sm text-gray-500 mt-5">
          Already have an account?
          <RouterLink :to="{ name: 'login' }" class="text-blue-500 font-medium hover:text-blue-700"
            >Log In</RouterLink
          >
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { authService } from '@/services/auth_service'
import { patterns } from '@/Validation'


const form = ref({ email: '', password: '', username: '', first_name: '', last_name: '' })
const loading = ref(false)
const error = ref('')
const success = ref('')

const handleRegister = async () => {
  error.value = ''
  loading.value = true
  try {
    if(!patterns.email.test(form.value.email) || form.value.email === ''){
    error.value = 'Please fill the email field.'
    return;
    }
    if(!patterns.name.test(form.value.username) || form.value.username === ''){
      error.value = 'Please fill the username field.'
      return;
    }
    if(!patterns.password.test(form.value.password) || form.value.password === ''){
      error.value = 'Please fill the password field. 6+ charachters.'
      return;
    }
    if(!patterns.name.test(form.value.first_name) || form.value.first_name === ''){
      error.value = 'Please fill the first name field.'
      return;
    }
    if(!patterns.name.test(form.value.last_name) || form.value.last_name === ''){
      error.value = 'Please fill the last name field.'
      return;
    }
    const response = await authService.register(
      form.value.username,
      form.value.email,
      form.value.password,
      form.value.first_name,
      form.value.last_name,
    )
    success.value = response?.message || "Account created!";
  } catch (e: any) {
    if(e.response.data.message){
      error.value = e.response?.data?.message
    } else{
      error.value = e.response?.data?.detail ?? 'Register failed. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>
