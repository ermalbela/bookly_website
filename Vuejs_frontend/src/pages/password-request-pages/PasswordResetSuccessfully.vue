<template>
  <div>
    <h1>
      Password Reset Successfully, Please <RouterLink :to="{ name: 'login' }" class="text-sm text-blue-500 hover:text-blue-700 border-b-2 border-blue-700">Log In</RouterLink>
    </h1>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>
