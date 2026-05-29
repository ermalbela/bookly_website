<template>
  <div class="py-12 px-12 bg-white rounded-sm shadow-sm">
    <div class="flex flex-col md:flex-col md:items-end md:justify-between mb-8">
      <div class="flex justify-between flex-row w-full">
        <h1 class="text-3xl font-bold">Books</h1>
        <input
          type="text"
          placeholder="Search books..."
          class="bg-white border-gray-500 px-4 py-2 border rounded-lg shadow-sm 
          focus:outline-none focus:ring-2 focus:ring-indigo-500 w-full md:w-64"
        />
      </div>

      <div class="mt-4 flex justify-end">
        <button v-if="authStore?.user?.role === 'admin'"
          class="px-4 py-3 bg-emerald-800 text-white text-sm font-medium rounded-md 
          cursor-pointer active:bg-emerald-900"
          @click="formModal?.open()"
        >
          Add Book
        </button>
      </div>
    </div>
    <div class="border-gray-300 border rounded-sm border-l p-5">
      <div
        v-if="loading"
        class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
      >
        <SkeletonBooks v-for="i in 8" :key="i" />
      </div>

      <div v-else-if="error" class="bg-red-100 text-red-700 p-4 rounded-lg">
        {{ error }}
      </div>

      <div v-else-if="books.length === 0" class="text-center py-20 bg-white rounded-xl shadow-sm">
        <h2 class="text-xl font-semibold text-gray-800">No books yet</h2>
        <p class="text-gray-500 mt-2">Add your first book to start building your library</p>
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div
          v-for="book in books"
          :key="book.uid"
          class="bg-white rounded-xl shadow-sm hover:shadow-lg transition-all duration-300 overflow-hidden group"
        >
          <div class="h-2"></div>
          <div class="p-5 flex flex-col h-full">
            <div class="flex justify-between">
              <h2 class="text-lg font-semibold text-gray-900transition">
                {{ book.title }}
              </h2>
              <button class="text-red-500 cursor-pointer" @click="handleDeleteBook(book.uid)">
                <i class="pi pi-times-circle" style="font-size: 1.3rem"></i>
              </button>
            </div>

            <p class="text-sm text-gray-500 mt-1">by {{ book.author }}</p>

            <div class="mt-4 space-y-1 text-sm text-gray-600">
              <p><span class="font-medium">Publisher:</span> {{ book.publisher }}</p>
              <p><span class="font-medium">Pages:</span> {{ book.page_count }}</p>
              <p><span class="font-medium">Language:</span> {{ book.language }}</p>
            </div>

            <div class="mt-auto pt-4 flex items-center justify-between">
              <span class="text-xs text-gray-400">
                {{ book.published_date.split('T')[0] }}
              </span>

              <RouterLink
                :to="{ name: 'book_detail', params: { id: book.uid } }"
                class="text-sm font-medium text-white outline-blue-600 bg-blue-600
                hover:bg-blue-700 hover:cursor-pointer rounded-md px-3 py-1 text-center active:bg-blue-900"
              >
                View
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>

    <FormModal ref="formModal" @save="handleSave" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { bookService } from '@/services/book_service'
import type { Book, BookCreateModel } from '@/types/book_types'
import SkeletonBooks from '@/components/SkeletonUI/SkeletonBooks.vue'
import FormModal from '@/components/modals/FormModal.vue'
import { useAuthStore } from '@/stores/auth_store'
import { useToastNotifications } from '@/_helper/useToastNotifications'

const authStore = useAuthStore();
const toastNotifications = useToastNotifications();

const books = ref<Book[]>([])
const loading = ref(true)
const error = ref('')

const formModal = ref<InstanceType<typeof FormModal>>()

const handleSave = async (book_data: BookCreateModel) => {
  try {
    const response = await bookService.create_book(book_data)
    books.value = await bookService.get_all_books();
    console.log(response)
  } catch (e: any) {
    console.log(e.response)
    toastNotifications.addToastNotifications(e.response.data.message ?? 'Something went wrong.', 'red');
  }
}

const handleDeleteBook = async (book_uid: string) => {
  if(!book_uid) return;

  try{
    await bookService.delete_book(book_uid);
    toastNotifications.addToastNotifications('Book deleted successfully.', 'green')
    books.value = await bookService.get_all_books();
  } catch(e: any){
    console.log(e.response)
    toastNotifications.addToastNotifications(e.response.data.message ?? 'Book Not found', 'red')
  }
}


onMounted(async () => {
  try {
    books.value = await bookService.get_all_books()
  } catch (e: any) {
    error.value = 'Failed to load books'
  } finally {
    loading.value = false
  }
})

</script>
