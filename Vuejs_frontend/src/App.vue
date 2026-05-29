<template>
  <RouterView />
  <ToastNotifications />
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router';
import { useAuthStore } from './stores/auth_store';
import ToastNotifications from './components/ToastNotifications.vue';


const auth = useAuthStore();
await auth.initAuth();

</script>