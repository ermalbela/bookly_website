<template>
  <div class="py-12 px-12 bg-white rounded-sm shadow-sm">
    <div class="flex flex-col mb-8">
      <div class="flex justify-between flex-row w-full">
        <h1 class="text-3xl font-bold">Books</h1>
        <input v-model="searchQuery" type="text" placeholder="Search books..."
          class="bg-white border-gray-500 px-4 py-2 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 w-full md:w-64" />
      </div>

      <div :class="{ 'mt-4 flex w-full items-center': true, 'justify-between': authStore?.user?.role === 'admin', 'justify-start': authStore?.user?.role === 'user' }">
        <div class="grid grid-cols-5 gap-3">
          <button v-for="type in ['all', 'saved', 'unsaved']" :key="type"
            :class="{ 'px-4 py-3 text-white text-sm font-medium rounded-md cursor-pointer': true, 'bg-emerald-800': filterType === type, 'bg-emerald-500': filterType !== type }"
            @click="filterType = type">
            {{ type.charAt(0).toUpperCase() + type.slice(1) }}
          </button>
        </div>
        <button v-if="authStore?.user?.role === 'admin'"
          class="px-4 py-3 bg-emerald-800 text-white text-sm font-medium rounded-md cursor-pointer"
          @click="formModal?.open()">
          Add Book
        </button>
      </div>
    </div>

    <div v-if="error" class="bg-red-100 text-red-700 p-4 rounded-lg">{{ error }}</div>

    <BookGrid
      :books="filteredBooks"
      :loading="loading || isSearching"
      :show-delete="authStore?.user?.role === 'admin'"
      @delete="handleDeleteBook"
      @save="handleSaveBook"
      @unsave="handleUnsaveBook"
    />

    <FormModal ref="formModal" @save="handleSave" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { bookService } from '@/services/book_service'
import { authService } from '@/services/auth_service'
import type { Book, BookCreateModel } from '@/types/book_types'
import FormModal from '@/components/modals/FormModal.vue'
import { useAuthStore } from '@/stores/auth_store'
import { useToastNotifications } from '@/_helper/useToastNotifications'
import { useDebounce } from '@/_helper/useDebounce'
import BookGrid from '@/components/books/BookGrid.vue'

const authStore = useAuthStore()
const toastNotifications = useToastNotifications()

const books = ref<Book[]>([])
const loading = ref(true)
const error = ref('')

const isSearching = ref(false)
const searchQuery = ref('')
const filterType = ref<'all' | 'saved' | 'unsaved'>('all')
const debouncedSearch = useDebounce(searchQuery, 600)

const formModal = ref<InstanceType<typeof FormModal>>()

const refetchBooks = async () => {
  books.value = await bookService.get_all_books()
}

const handleSave = async (book_data: BookCreateModel) => {
  try {
    const response = await bookService.create_book(book_data)
    refetchBooks()
    console.log(response)
  } catch (e: any) {
    console.log(e.response)
    toastNotifications.addToastNotifications(
      e.response.data.message ?? 'Something went wrong.',
      'red',
    )
  }
}

const handleDeleteBook = async (book_uid: string) => {
  if (!book_uid) return

  try {
    await bookService.delete_book(book_uid)
    toastNotifications.addToastNotifications('Book deleted successfully.', 'green')
    refetchBooks()
  } catch (e: any) {
    console.log(e.response)
    toastNotifications.addToastNotifications(e.response.data.message ?? 'Book Not found', 'red')
  }
}

const handleSaveBook = async (book_uid: string) => {
  if (!book_uid || !authStore.user?.uid) return

  try {
    await authService.save_book(authStore.user.uid, book_uid)
    refetchBooks()
  } catch (e: any) {
    toastNotifications.addToastNotifications(
      e.response?.data?.detail ?? 'Something went wrong.',
      'red',
    )
  }
}

const handleUnsaveBook = async (book_uid: string) => {
  if (!book_uid || !authStore.user?.uid) return

  try {
    await authService.unsave_book(authStore.user.uid, book_uid)
    refetchBooks()
  } catch (e: any) {
    toastNotifications.addToastNotifications(
      e.response?.data?.detail ?? 'Something went wrong.',
      'red',
    )
  }
}

const filteredBooks = computed(() => {
  return books.value.filter((book) => {
    const matchesSearch =
      debouncedSearch.value.trim() === '' ||
      book.title.toLowerCase().includes(debouncedSearch.value.toLowerCase()) ||
      book.author.toLowerCase().includes(debouncedSearch.value.toLowerCase())

    const matchesFilter =
      filterType.value === 'all'
        ? true
        : filterType.value === 'saved'
          ? book.is_saved
          : filterType.value === 'unsaved'
            ? !book.is_saved
            : true

    return matchesSearch && matchesFilter
  })
})

onMounted(async () => {
  try {
    books.value = await bookService.get_all_books()
  } catch (e: any) {
    error.value = 'Failed to load books'
  } finally {
    loading.value = false
  }
})

watch(searchQuery, () => {
  isSearching.value = true
})

watch(debouncedSearch, () => {
  isSearching.value = false
})
</script>
