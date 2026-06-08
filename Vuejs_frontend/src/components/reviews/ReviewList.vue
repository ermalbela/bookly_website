<template>
  <div class="flex items-center justify-between">
    <h2 class="text-2xl font-semibold text-gray-900">
      <slot name="header">Reviews</slot>
    </h2>
    <slot name="action"></slot>
    <!-- slot for addreview button -->
  </div>
  <div class="mb-8 border border-gray-300 p-7">
    <div class="bg-white rounded-2xl shadow-sm p-8">
      <div v-if="reviews.length === 0" class="text-center py-10 text-gray-400">
        <div class="text-4xl mb-3">...</div>
        <p class="text-sm">No reviews yet.</p>
      </div>

      <div v-else class="space-y-4">
        <ReviewCard
          v-for="review in reviews"
          :key="review.uid"
          :review="review"
          :can-delete="canDelete(review)"
          @delete="emit('delete', $event)"
          @like="emit('like', $event)"
          @unlike="emit('unlike', $event)"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Review } from '@/types/review_types'
import ReviewCard from './ReviewCard.vue'
import { useAuthStore } from '@/stores/auth_store'

defineProps<{
  reviews: Review[]
  canDelete?: boolean
}>()

const emit = defineEmits<{
  delete: [uid: string]
  like: [uid: string]
  unlike: [uid: string]
}>()

const authStore = useAuthStore()

const canDelete = (review: Review): boolean => {
  if (!authStore.user) return false
  return authStore.user.role === 'admin' || review.user_uid === authStore.user.uid
}
</script>
