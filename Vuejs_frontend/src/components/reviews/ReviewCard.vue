<template>
  <div class="p-5 bg-gray-50 rounded-xl border border-gray-100">
    <div class="flex items-center justify-between mb-3">
      <div class="flex items-center gap-2">
        <img
          :src="review.user?.avatar_url ?? '/default-avatar.png'"
          class="w-8 h-8 rounded-full object-cover"
        />
        <span class="text-sm font-medium text-gray-800">
          {{ review.user?.username ?? 'Deleted User' }}
        </span>
      </div>
      <div class="flex items-center gap-2">
        <span class="text-xs text-gray-400">{{ formatDate(review.created_at) }}</span>
        <button
          v-if="canDelete"
          @click="emit('delete', review.uid)"
          class="text-red-400 hover:text-red-600 transition-colors cursor-pointer"
        >
          <i class="pi pi-times"></i>
        </button>
      </div>
    </div>

    <div class="flex gap-0.5 mb-2">
      <span v-for="i in 5" :key="i" class="text-base"
        :class="i <= review.rating ? 'text-yellow-400' : 'text-gray-200'">★</span>
    </div>

    <p class="text-sm text-gray-700 leading-relaxed">{{ review.review_text }}</p>

    <div class="flex items-center gap-1 mt-3">
      <button
        @click="() => {
          if (review.is_liked) {
            emit('unlike', review.uid)
          } else {
            emit('like', review.uid)
          }
        }"
        :class="review.is_liked ? 'text-red-500' : 'text-gray-400'"
        class="transition-colors cursor-pointer"
      >
        <i :class="review.is_liked ? 'pi pi-heart-fill' : 'pi pi-heart'"></i>
      </button>
      <span class="text-xs text-gray-500">{{ review.likes_count }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Review } from '@/types/review_types'

defineProps<{
  review: Review
  canDelete?: boolean
}>()

const emit = defineEmits<{
  delete: [uid: string]
  like: [uid: string]
  unlike: [uid: string]
}>()


const formatDate = (iso: string) =>
  new Date(iso).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
</script>