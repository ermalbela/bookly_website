<template>
  <div class="py-12 px-12 bg-white rounded-sm shadow-sm">
    <div class="flex flex-col md:flex-col md:items-end md:justify-between mb-8">
      <div class="flex justify-between flex-row w-full">
        <h1 class="text-3xl font-bold">Book</h1>
        <RouterLink
          :to="{ name: 'books' }"
          class="inline-flex items-center gap-1.5 text-sm text-gray-400 hover:text-gray-700 transition-colors"
        >
          Back to Books
        </RouterLink>
      </div>
    </div>

    <div v-if="loading" class="flex items-center justify-center h-64">
      <div class="text-gray-400 animate-pulse">Loading book...</div>
    </div>

    <div v-else-if="error" class="bg-red-50 text-red-600 p-4 rounded-xl">{{ error }}</div>

    <div v-else-if="book" class="mx-auto space-y-6">
      <div class="border-gray-300 border rounded-sm border-l p-5 grid gap-4">
        <div class="flex w-full justify-between">
          <div class="flex items-center justify-between">
            <h2 class="text-2xl font-semibold text-gray-900">
              Book Details
            </h2>
          </div>
          <button
            v-if="authStore.user?.role === 'admin'"
            @click="tagIsOpen = true"
            class="px-4 py-3 bg-emerald-800 text-white text-sm font-medium rounded-md cursor-pointer active:bg-emerald-900"
          >
            Add Tag
          </button>
        </div>
        <div class="mb-8 border border-gray-300 p-7">
          <div class="bg-white rounded-2xl shadow-sm overflow-hidden mb-4">
            <div class="flex flex-col md:flex-row md:items-start md:justify-between p-8">
              <div class="flex-1">
                <h1 class="text-3xl font-bold text-gray-900 leading-tight">{{ book.title }}</h1>
                <p class="text-lg text-gray-500 mt-1">
                  by <span class="text-gray-700 font-medium">{{ book.author }}</span>
                </p>
                <div class="flex flex-wrap gap-2 mt-4">
                  <span
                    v-for="tag in book.tags"
                    :key="tag.uid"
                    class="text-xs font-medium px-3 py-1 bg-blue-50 text-blue-600 rounded-full border border-blue-100"
                  >
                    {{ tag.name }}
                    <button
                      class="ml-2 text-red-500 cursor-pointer active:text-red-900"
                      @click="handleRemoveTagFromBook(book.uid, tag.uid)"
                    >
                      <i class="pi pi-times-circle"></i>
                    </button>
                  </span>
                  <span v-if="book.tags.length === 0" class="text-xs text-gray-400">No tags</span>
                </div>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-5">
            <div
              v-for="detail in details"
              :key="detail.label"
              class="bg-white rounded-xl shadow-sm p-5 border border-gray-50"
            >
              <p class="text-xs text-gray-400 font-medium uppercase tracking-wide">
                {{ detail.label }}
              </p>
              <p class="text-sm font-semibold text-gray-800 mt-1">{{ detail.value }}</p>
            </div>
          </div>
        </div>
        <ReviewList
          :reviews="book.reviews"
          @delete="deleteReview"
          @like="likeReview"
          @unlike="unlikeReview"
        >
          <template #action>
            <button
              v-if="!hasReviewed"
              @click="rateModal?.open()"
              class="px-4 py-3 bg-emerald-800 text-white text-sm font-medium rounded-md cursor-pointer"
              >
              Add Review
            </button>
            <p v-else class="text-sm text-gray-400">You already reviewed this book</p>
          </template>
        </ReviewList>
      </div>
    </div>
  </div>

  <RateModal
    ref="rateModal"
    @submit="({ rating, review_text }) => submitReview(rating, review_text)"
  />
  <CommonModal v-model="tagIsOpen" title="Add Tag" size="md">
     <div class="relative h-40 scrollbar-gutter-stable">
      <label class="text-sm font-medium text-gray-700">Tag Name</label>
      <input
        v-model="tagQuery"
        type="text"
        class="mt-1 w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Search tags..."
        @focus="tagDropdown = true"
        @blur="handleBlur"
      />
      <ul
        v-if="tagDropdown && filteredTags.length > 0"
        class="absolute z-10 mt-1 w-full bg-white border border-gray-200 rounded-lg shadow-md block overflow-y-auto"
      >
        <li
          v-for="tag in filteredTags"
          :key="tag.uid"
          @mousedown.prevent="selectTag(tag)"
          class="px-3 py-2 text-sm text-gray-700 cursor-pointer hover:bg-blue-50 hover:text-blue-600"
        >
          {{ tag.name }}
        </li>
      </ul>
      <div v-else-if="filteredTags.length === 0" class="mt-1 w-full flex justify-center">No Tags...</div>
    </div>

    <template #footer>
      <button
        @click="tagIsOpen = false"
        class="px-4 py-2 text-sm font-medium rounded-lg text-gray-800 bg-gray-300 cursor-pointer"
      >
        Cancel
      </button>
      <button
        class="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 cursor-pointer"
        @click="addTag(book?.uid, tagValue?.uid)"
      >
        Add Tag
      </button>
    </template>
  </CommonModal>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { bookService } from '@/services/book_service'
import type { BookDetail } from '@/types/book_types'
import RateModal from '@/components/modals/RateModal.vue'
import { reviewService } from '@/services/review_service'
import CommonModal from '@/components/modals/CommonModal.vue'
import { tagService } from '@/services/tag_service'
import { useToastNotifications } from '@/_helper/useToastNotifications'
import { useAuthStore } from '@/stores/auth_store'
import ReviewList from '@/components/reviews/ReviewList.vue'

const authStore = useAuthStore();
const toastNotifications = useToastNotifications();
const route = useRoute()
const book = ref<BookDetail | null>(null)
const tags = ref<{ name: string; uid: string }[]>([])
const loading = ref(true)
const error = ref('')

const tagQuery = ref('')
const tagIsOpen = ref(false)
const tagValue = ref<{ name: string; uid: string } | null>(null)
const tagDropdown = ref(false)
const rateModal = ref<InstanceType<typeof RateModal>>()

onMounted(async () => {
  try {
    book.value = await bookService.get_book_by_id(route.params.id as string)
    tags.value = await tagService.get_all_tags()
  } catch {
    error.value = 'Failed to load book details.'
  } finally {
    loading.value = false
  }
})

const refetchBook = async () => {
  book.value = await bookService.get_book_by_id(route.params.id as string)
}

const details = computed(() => {
  if (!book.value) return []
  return [
    { label: 'Publisher', value: book.value.publisher },
    { label: 'Published', value: book.value.published_date.split('T')[0] },
    { label: 'Pages', value: book.value.page_count.toLocaleString() },
    { label: 'Language', value: book.value.language },
  ]
})

const submitReview = async (rating: number, review_text: string) => {
  if (!book.value) return
  
  try {
    await reviewService.create_review(rating, review_text, book.value?.uid)
    refetchBook();
    toastNotifications.addToastNotifications('Review submitted successfully!', 'green')
    rateModal.value?.close()
  } catch (e: any) {
    console.log(e.response.data.detail)
    toastNotifications.addToastNotifications(e.response.data?.detail ?? 'Something went wrong.', 'red')
  }
}

const likeReview = async (review_uid: string) => {
  if(!authStore.user?.uid || !review_uid) return;

  try{
    await reviewService.like_review(review_uid, authStore.user?.uid);
    refetchBook();
  } catch(e: any){
    toastNotifications.addToastNotifications(e.response?.data?.detail ?? 'Something went wrong.', 'red', 5000)
  }
}

const unlikeReview = async (review_uid: string) => {
  if(!authStore.user?.uid || !review_uid) return;

  try{
    await reviewService.unlike_review(review_uid, authStore.user?.uid);
    refetchBook();
  } catch(e: any){
    toastNotifications.addToastNotifications(e.response?.data?.detail ?? 'Something went wrong.', 'red', 5000)
  }
}

const deleteReview = async (review_uid: string) => {
  if(!review_uid) return;
  
  try{
    await reviewService.delete_review(review_uid);
    refetchBook();
    toastNotifications.addToastNotifications('Review deleted successfully.', 'green');
  } catch(e: any){
    toastNotifications.addToastNotifications(e.response?.data?.detail ?? 'Something went wrong.', 'red', 5000);
  }
}

const addTag = async (book_uid?: string, tag_uid?: string) => {
  if (!book_uid || !tag_uid || !tagQuery.value) {
    toastNotifications.addToastNotifications('Please add a tag.', 'red')
    return
  }

  try {
    await tagService.add_tag_to_book(book_uid, tag_uid)

    tagIsOpen.value = false
    tagValue.value = null
    tagQuery.value = '';
    refetchBook();
    toastNotifications.addToastNotifications('Tag added successfully!', 'green')
  } catch (e: any) {
    toastNotifications.addToastNotifications(e.response?.data?.detail ?? 'Something went wrong.', 'red')
  }
}

const handleBlur = () => {
  setTimeout(() => {
    tagDropdown.value = false
  }, 100)
}

const filteredTags = computed(() =>
  tags.value.filter((tag) => tag.name.toLowerCase().includes(tagQuery.value.toLowerCase())),
)

const selectTag = (tag: { uid: string; name: string }) => {
  tagValue.value = tag
  tagQuery.value = tag.name
  tagDropdown.value = false
}

const handleRemoveTagFromBook = async (book_uid: string, tag_uid: string) => {
  if (!tag_uid || !book_uid) return

  try {
    await tagService.remove_tag_from_book(book_uid, tag_uid)
    toastNotifications.addToastNotifications('Tag removed successfully', 'green')
    refetchBook();
  } catch (e: any) {
    console.log(e.response.data)
    toastNotifications.addToastNotifications(e.response?.data?.detail ?? 'Something went wrong.', 'red', 5000)
  }
}

const hasReviewed = computed(() =>
  book.value?.reviews.some(r => r.user_uid === authStore.user?.uid) ?? false
)

watch(tagQuery, (val) => {
  if (tagValue.value && val !== tagValue.value.name) {
    tagValue.value = null
  }
})

</script>
