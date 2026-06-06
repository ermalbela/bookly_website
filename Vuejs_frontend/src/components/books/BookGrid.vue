<template>
  <div class="border-gray-300 border rounded-sm border-l p-5">
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      <SkeletonBooks v-for="i in 8" :key="i" />
    </div>
    
    <div v-else-if="books.length === 0" class="text-center py-20 bg-white rounded-xl shadow-sm">
      <h2 class="text-xl font-semibold text-gray-800">No books found</h2>
      <p class="text-gray-500 mt-2">Add more books to keep building your library</p>
    </div>
    
    <div v-else class="flex items-center justify-start">
      <h2 class="text-2xl font-semibold text-gray-900 mb-4">Published Books</h2>
    </div>
    <div class="border border-gray-300 p-7">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <BookCard
          v-for="book in books"
          :key="book.uid"
          :book="book"
          :show-delete="showDelete"
          @delete="emit('delete', $event)"
          @save="emit('save', $event)"
          @unsave="emit('unsave', $event)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Book } from '@/types/book_types'
import BookCard from './BookCard.vue'
import SkeletonBooks from '@/components/SkeletonUI/SkeletonBooks.vue'

defineProps<{
  books: Book[]
  loading?: boolean
  showDelete?: boolean
}>()

const emit = defineEmits<{
  delete: [uid: string]
  save: [uid: string]
  unsave: [uid: string]
}>()
</script>