<template>
  <div class="bg-white rounded-xl shadow-sm hover:shadow-lg transition-all duration-300 overflow-hidden">
    <div class="h-2"></div>
    <div class="p-5 flex flex-col h-full">
      <div class="flex justify-between">
        <h2 class="text-lg font-semibold text-gray-900">{{ book.title }}</h2>
        <button v-if="showDelete" class="text-red-500 cursor-pointer" @click="emit('delete', book.uid)">
          <i class="pi pi-times-circle" style="font-size: 1.3rem"></i>
        </button>
      </div>

      <p class="text-sm text-gray-500 mt-1">by {{ book.author }}</p>

      <div class="mt-4 space-y-1 text-sm text-gray-600">
        <p><span class="font-medium">Publisher:</span> {{ book.publisher }}</p>
        <p><span class="font-medium">Pages:</span> {{ book.page_count }}</p>
        <p><span class="font-medium">Language:</span> {{ book.language }}</p>
      </div>

      <div class="flex justify-end">
        <button v-if="book.is_saved" @click="emit('unsave', book.uid)" class="text-yellow-500 cursor-pointer active:text-yellow-700">
          <i class="pi pi-bookmark-fill"></i>
        </button>
        <button v-else @click="emit('save', book.uid)" class="text-yellow-500 cursor-pointer active:text-yellow-700">
          <i class="pi pi-bookmark"></i>
        </button>
      </div>

      <div class="mt-auto pt-2 flex items-center justify-between">
        <span class="text-xs text-gray-400">{{ book.published_date.split('T')[0] }}</span>
        <RouterLink
          :to="{ name: 'book_detail', params: { id: book.uid } }"
          class="text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md px-3 py-1 active:bg-blue-900"
        >
          View
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Book } from '@/types/book_types'

defineProps<{
  book: Book
  showDelete?: boolean
}>()

const emit = defineEmits<{
  delete: [uid: string]
  save: [uid: string]
  unsave: [uid: string]
}>()
</script>