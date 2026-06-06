<template>
  <div class="py-12 px-12 bg-white rounded-sm shadow-sm space-y-8">
    <div class="mx-auto space-y-6">
      <h1 class="text-3xl font-bold">User Profile</h1>
      <div class="border-gray-300 border rounded-sm border-l p-5 grid gap-4">

        <div v-if="loading" class="space-y-8">
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <SkeletonBooks v-for="i in 4" :key="i" />
          </div>
        </div>

        <div v-else-if="error" class="bg-red-100 text-red-700 p-4 rounded-lg">{{ error }}</div>

        <template v-else>
          <h2 class="text-2xl font-semibold text-gray-900">Saved Books</h2>
          <div class="border-gray-300 border rounded-sm border-l p-5 mb-8">
            <div class="flex items-center justify-between mb-6">
            </div>
            <div v-if="profile.saved_books.length === 0" class="text-center py-10 text-gray-400">
              <p class="text-sm">No saved books yet.</p>
            </div>
            <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              <BookCard
                v-for="book in profile.saved_books"
                :key="book.uid"
                :book="book"
                :show-delete="false"
                @save="handleSaveBook"
                @unsave="handleUnsaveBook"
              />
            </div>
          </div>

            <ReviewList
              :reviews="profile.reviews"
              @delete="deleteReview"
              @like="likeReview"
              @unlike="unlikeReview"
            >
              <template #header>My Reviews</template>
            </ReviewList>

            <ReviewList
              :reviews="profile.liked_reviews"
              @unlike="unlikeReview"
              @like="likeReview"
              @delete="deleteReview"
            >
              <template #header>Liked Reviews</template>
            </ReviewList>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { authService } from '@/services/auth_service'
import { useAuthStore } from '@/stores/auth_store'
import { useToastNotifications } from '@/_helper/useToastNotifications'
import { reviewService } from '@/services/review_service'
import SkeletonBooks from '@/components/SkeletonUI/SkeletonBooks.vue'
import BookCard from '@/components/books/BookCard.vue'
import ReviewList from '@/components/reviews/ReviewList.vue'
import type { Review } from '@/types/review_types'
import type { Book } from '@/types/book_types'

const authStore = useAuthStore()
const toastNotifications = useToastNotifications()

const loading = ref(true)
const error = ref('')

const profile = ref<{
  saved_books: Book[]
  reviews: Review[]
  liked_reviews: Review[]
}>({
  saved_books: [],
  reviews: [],
  liked_reviews: [],
})

const refetchProfile = async () => {
  profile.value = await authService.get_profile()
}

onMounted(async () => {
  try {
    await refetchProfile()
  } catch (e: any) {
    error.value = 'Failed to load profile.'
  } finally {
    loading.value = false
  }
})

const handleSaveBook = async (book_uid: string) => {
  if (!authStore.user?.uid) return
  try {
    await authService.save_book(authStore.user.uid, book_uid)
    await refetchProfile()
  } catch (e: any) {
    toastNotifications.addToastNotifications(e.response?.data?.detail ?? 'Something went wrong.', 'red')
  }
}

const handleUnsaveBook = async (book_uid: string) => {
  if (!authStore.user?.uid) return
  try {
    await authService.unsave_book(authStore.user.uid, book_uid)
    await refetchProfile()
  } catch (e: any) {
    toastNotifications.addToastNotifications(e.response?.data?.detail ?? 'Something went wrong.', 'red')
  }
}


const likeReview = async (review_uid: string) => {
  if(!authStore.user?.uid || !review_uid) return;

  try{
    await reviewService.like_review(review_uid, authStore.user?.uid);
    refetchProfile();
  } catch(e: any){
    toastNotifications.addToastNotifications(e.response?.data?.detail ?? 'Something went wrong.', 'red', 5000)
  }
}

const unlikeReview = async (review_uid: string) => {
  if(!authStore.user?.uid || !review_uid) return;

  try{
    await reviewService.unlike_review(review_uid, authStore.user?.uid);
    toastNotifications.addToastNotifications('Unliked successfully!', 'green')
    refetchProfile();
  } catch(e: any){
    toastNotifications.addToastNotifications(e.response?.data?.detail ?? 'Something went wrong.', 'red', 5000)
  }
}

const deleteReview = async (review_uid: string) => {
  if(!review_uid) return;
  
  try{
    await reviewService.delete_review(review_uid);
    refetchProfile();
    toastNotifications.addToastNotifications('Review deleted successfully.', 'green');
  } catch(e: any){
    toastNotifications.addToastNotifications(e.response?.data?.detail ?? 'Something went wrong.', 'red', 5000);
  }
}

</script>