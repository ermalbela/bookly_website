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
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4">
              <img
                :src="profile.user.avatar_url"
                class="border-3 border-blue-300 w-30 h-30 rounded-full object-cover"
              />
              <div>
                <h2 class="text-2xl font-bold text-gray-900">{{ profile.user.username }}</h2>
                <p class="text-sm text-gray-500">
                  {{ profile.user.first_name }} {{ profile.user.last_name }}
                </p>
                <div class="flex gap-4 mt-2 text-sm text-gray-500">
                  <span>
                    <strong class="text-gray-900">{{ profile.followers_count }}</strong>
                    followers
                  </span>
                  <span
                    ><strong class="text-gray-900">{{ profile.following_count }}</strong>
                    following</span
                  >
                </div>
              </div>
            </div>

            <button
              v-if="!isOwnProfile"
              @click="toggleFollow"
              :class="{
                'px-5 py-2 text-sm font-medium rounded-md cursor-pointer transition-colors': true,
                'bg-blue-600 text-white hover:bg-blue-700': !profile.is_following,
                'bg-gray-200 text-gray-700 hover:bg-gray-300': profile.is_following,
              }"
            >
              {{ profile.is_following ? 'Unfollow' : 'Follow' }}
            </button>
          </div>

          <h2 class="text-2xl font-semibold text-gray-900">Saved Books</h2>
          <div class="border-gray-300 border rounded-sm border-l p-5 mb-8">
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
            <template #header>Submitted Reviews</template>
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
import { ref, onMounted, computed, watch } from 'vue'
import { authService } from '@/services/auth_service'
import { useAuthStore } from '@/stores/auth_store'
import { useToastNotifications } from '@/_helper/useToastNotifications'
import { reviewService } from '@/services/review_service'
import SkeletonBooks from '@/components/SkeletonUI/SkeletonBooks.vue'
import BookCard from '@/components/books/BookCard.vue'
import ReviewList from '@/components/reviews/ReviewList.vue'
import { useRoute } from 'vue-router'
import type { ProfileResponse } from '@/types/user_types'

const authStore = useAuthStore()
const toastNotifications = useToastNotifications()
const route = useRoute()

const profileUid = computed(() => (route.params.uid as string) || authStore.user?.uid)
const isOwnProfile = computed(() => profileUid.value === authStore.user?.uid)

const loading = ref(true)
const error = ref('')

const profile = ref<ProfileResponse>({
  saved_books: [],
  reviews: [],
  liked_reviews: [],
  is_following: false,
  followers_count: 0,
  following_count: 0,
  user: {
    username: '',
    first_name: '',
    last_name: '',
    avatar_url: '',
  },
})

const refetchProfile = async () => {
  if (!profileUid.value) return
  profile.value = await authService.get_user_profile(profileUid.value)
}

const handleSaveBook = async (book_uid: string) => {
  if (!authStore.user?.uid) return
  try {
    await authService.save_book(authStore.user.uid, book_uid)
    await refetchProfile()
  } catch (e: any) {
    toastNotifications.addToastNotifications(
      e.response?.data?.detail ?? 'Something went wrong.',
      'red',
    )
  }
}

const handleUnsaveBook = async (book_uid: string) => {
  if (!authStore.user?.uid) return
  try {
    await authService.unsave_book(authStore.user.uid, book_uid)
    await refetchProfile()
  } catch (e: any) {
    toastNotifications.addToastNotifications(
      e.response?.data?.detail ?? 'Something went wrong.',
      'red',
    )
  }
}

const likeReview = async (review_uid: string) => {
  if (!authStore.user?.uid || !review_uid) return

  try {
    await reviewService.like_review(review_uid, authStore.user?.uid)
    refetchProfile()
  } catch (e: any) {
    toastNotifications.addToastNotifications(
      e.response?.data?.detail ?? 'Something went wrong.',
      'red',
      5000,
    )
  }
}

const unlikeReview = async (review_uid: string) => {
  if (!authStore.user?.uid || !review_uid) return

  try {
    await reviewService.unlike_review(review_uid, authStore.user?.uid)
    toastNotifications.addToastNotifications('Unliked successfully!', 'green')
    refetchProfile()
  } catch (e: any) {
    toastNotifications.addToastNotifications(
      e.response?.data?.detail ?? 'Something went wrong.',
      'red',
      5000,
    )
  }
}


const deleteReview = async (review_uid: string) => {
  if (!review_uid) return

  try {
    await reviewService.delete_review(review_uid)
    refetchProfile()
    toastNotifications.addToastNotifications('Review deleted successfully.', 'green')
  } catch (e: any) {
    toastNotifications.addToastNotifications(
      e.response?.data?.detail ?? 'Something went wrong.',
      'red',
      5000,
    )
  }
}

const toggleFollow = async () => {
  if (!profileUid.value) return
  try {
    if (profile.value.is_following) {
      await authService.unfollow_user(profileUid.value)
    } else {
      await authService.follow_user(profileUid.value)
    }
    await refetchProfile()
  } catch (e: any) {
    toastNotifications.addToastNotifications(
      e.response?.data?.detail ?? 'Something went wrong.',
      'red',
      5000,
    )
  }
}

const loadProfile = async () => {
  loading.value = true
  error.value = ''
  try {
    await refetchProfile()
  } catch {
    error.value = 'Failed to load profile.'
  } finally {
    loading.value = false
  }
}

onMounted(loadProfile)

watch(() => route.params.uid, loadProfile)

</script>
