<template>
  <div class="min-h-screen bg-slate-200 flex flex-col items-center justify-center px-4 py-12">

    <div class="w-full max-w-xl bg-white rounded-2xl shadow-sm border border-gray-300 p-8">
      <RouterView />
    </div>

    <p class="text-xs text-gray-600 mt-6">{{ year }} Bookly. All rights reserved.</p>

  </div>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()
</script>