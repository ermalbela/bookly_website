<template>
  <header class="h-16 bg-white border-b border-gray-300 flex items-center px-6 font-bold text-lg tracking-widest shadow-sm w-full z-10 justify-between">
    <h1 class="text-3xl ml-9 text-blue-500 ">BOOKLY</h1>
    <div class="w-full flex justify-end items-center">
      <button class="px-3 py-2 bg-emerald-800 text-white text-sm font-medium rounded-md cursor-pointer active:bg-emerald-900" @click="handleLogout()">LOG OUT</button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth_store';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();

const router = useRouter();

const handleLogout = async () => {
  try{
    await authStore.logout();
    await router.push({name: 'login'});
  } catch(e){
    console.log(e);
  }
}

</script>