<template>
  <div class="flex w-full h-full min-h-screen justify-center items-center flex-col">
    <h1 class="text-5xl font-bold uppercase">404 - Page not found!</h1>
    <RouterLink to="/books" class="text-blue-500 text-3xl mt-5 uppercase font-semibold">Back to home</RouterLink>
  </div>

</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router';

</script>