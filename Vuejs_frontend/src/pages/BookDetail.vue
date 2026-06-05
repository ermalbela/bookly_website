<template>
  <div class="py-12 px-12 bg-white rounded-sm shadow-sm">
    <div class="flex flex-col md:flex-col md:items-end md:justify-between mb-8">
      <div class="flex justify-between flex-row w-full">
        <h1 class="text-3xl font-bold">Books</h1>
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
          <button
            @click="tagIsOpen = true"
            class="px-4 py-3 bg-emerald-800 text-white text-sm font-medium rounded-md cursor-pointer active:bg-emerald-900"
          >
            Add Tag
          </button>
          <button
            @click="rateModal?.open()"
            class="px-4 py-3 bg-emerald-800 text-white text-sm font-medium rounded-md cursor-pointer active:bg-emerald-900"
          >
            Add Review
          </button>
        </div>
        <div class="bg-white rounded-2xl shadow-sm overflow-hidden">
          <div class="p-8">
            <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-6">
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

              <div
                class="flex flex-col items-center justify-center bg-gray-50 rounded-xl px-6 py-4 border border-gray-100 min-w-28"
              >
                <span class="text-3xl font-bold text-gray-900">{{ avgRating }}</span>
                <div class="flex gap-0.5 mt-1">
                  <span
                    v-for="n in 5"
                    :key="n"
                    class="text-lg"
                    :class="n <= Math.round(avgRating) ? 'text-yellow-400' : 'text-gray-200'"
                    >★</span
                  >
                </div>
                <span class="text-xs text-gray-400 mt-1"
                  >{{ book.reviews.length }} review{{ book.reviews.length !== 1 ? 's' : '' }}</span
                >
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
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

        <div class="bg-white rounded-2xl shadow-sm p-8">
          <h2 class="text-lg font-semibold text-gray-900 mb-6">Reviews</h2>

          <div v-if="book.reviews.length === 0" class="text-center py-10 text-gray-400">
            <div class="text-4xl mb-3">💬</div>
            <p class="text-sm">No reviews yet for this book.</p>
          </div>

          <div v-else class="space-y-4">
            <div
              v-for="review in book.reviews"
              :key="review.uid"
              class="p-5 bg-gray-50 rounded-xl border border-gray-100"
            >
              <div class="flex items-start justify-between mb-3">
                <div>
                  <div class="flex flex-col">
                    <span class="text-xs text-gray-400 mb-4">{{ review.user?.username ?? 'deleted_user' }}</span>
                  </div>
                  <div class="flex gap-0.5">
                    <span
                      v-for="i in 5"
                      :key="i"
                      class="text-base"
                      :class="i <= review.rating ? 'text-yellow-400' : 'text-gray-200'"
                      >
                      ★
                    </span>
                  </div>
                </div>
                <div class="flex flex-col">
                  <button 
                    v-if="canDeleteReview(review)" 
                    class="text-red-500 cursor-pointer active:text-red-900 w-fit self-end mb-4"
                    @click="deleteReview(review.uid)"
                    >
                    <i class="pi pi-times-circle"></i>
                  </button>
                  <span class="text-xs text-gray-400 h-full text-start">{{ formatDate(review.created_at) }}</span>
                </div>
              </div>
              <div class="flex justify-between">
                <p class="text-sm text-gray-700 leading-relaxed">{{ review.review_text }}</p>
                <div class="flex flex-column">
                  <span class="text-sm mr-3 text-gray-600">{{ review.likes_count }}</span>
                  <button 
                      v-if="review.is_liked"
                      class="text-red-500 cursor-pointer active:text-red-900 w-fit self-end mb-4"
                      @click="unlikeReview(review.uid)"
                      >
                      <i class="pi pi-heart-fill"></i>
                  </button>
                  <button 
                      v-else
                      class="text-red-500 cursor-pointer active:text-red-900 w-fit self-end mb-4"
                      @click="likeReview(review.uid)"
                      >
                      <i class="pi pi-heart"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
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
import type { Review } from '@/types/review_types'
import { useAuthStore } from '@/stores/auth_store'

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

const avgRating = computed(() => {
  if (!book.value?.reviews.length) return 0
  const sum = book.value.reviews.reduce((acc, r) => acc + r.rating, 0)
  return Number((sum / book.value.reviews.length).toFixed(1))
})

const details = computed(() => {
  if (!book.value) return []
  return [
    { label: 'Publisher', value: book.value.publisher },
    { label: 'Published', value: book.value.published_date.split('T')[0] },
    { label: 'Pages', value: book.value.page_count.toLocaleString() },
    { label: 'Language', value: book.value.language },
  ]
})

const canDeleteReview = (review: Review): boolean => {
  if(!authStore.user) return false;
  return authStore.user.role === 'admin' || review.user_uid === authStore.user.uid
}

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

watch(tagQuery, (val) => {
  if (tagValue.value && val !== tagValue.value.name) {
    tagValue.value = null
  }
})

const formatDate = (iso: string) =>
  new Date(iso).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
</script>
