<template>
  <MainContent />
</template>

<script setup lang="ts">
import MainContent from '@/components/MainContent.vue'

</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>