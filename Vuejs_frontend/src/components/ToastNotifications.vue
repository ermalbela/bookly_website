<template>
  <Teleport to="body">
    <ol
      class="fixed top-1 z-100 flex max-h-screen w-full flex-col-reverse p-4 sm:bottom-auto 
        sm:right-0 sm:top-15 sm:flex-col md:max-w-105"
    >
      <li
        v-for="notification in notifications"
        :key="notification.id"
        class="mb-4 pointer-events-auto relative flex w-full items-center justify-between space-x-2 
          overflow-hidden rounded-md p-4 pr-6 shadow-lg transition-all border"
        :class="{
          'bg-green-50 text-green-600': notification.color === 'green',
          'bg-red-100 text-red-700': notification.color === 'red'
        }"
      >
        <div class="text-sm font-semibold">
          {{ notification.message }}
        </div>
        <button
          @click="removeToastNotifications(notification.id)"
          class="inline-flex h-8 shrink-0 items-center justify-center rounded-md border bg-transparent
            px-3 text-sm font-medium transition-colors hover:bg-gray-200 focus:outline-none focus:ring-1 
           focus:ring-gray-300 disabled:pointer-events-none disabled:opacity-50"
        >
          OK
        </button>
      </li>
    </ol>
  </Teleport>
</template>

<script setup lang="ts">
import { useToastNotifications } from '@/_helper/useToastNotifications'

const { notifications, removeToastNotifications } = useToastNotifications()
</script>