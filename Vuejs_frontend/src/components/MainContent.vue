<template>
  <div class="flex flex-col h-screen overflow-hidden bg-slate-100">
    <AppNavbar />

    <div class="flex flex-1 overflow-hidden">
      <AppSidebar v-model:currentTab="currentTab" />

      <main class="flex-1 overflow-y-auto px-15 py-19">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref} from 'vue';
import AppNavbar from '@/components/AppNavbar.vue'
import AppSidebar from '@/components/AppSidebar.vue'
import { useRoute } from 'vue-router';

const route = useRoute();

const currentTab = ref(`${route.name?.toString().charAt(0).toUpperCase()}${route.name?.toString().slice(1, )}`)

</script>