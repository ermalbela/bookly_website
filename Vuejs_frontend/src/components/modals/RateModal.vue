<template>
  <CommonModal v-model="isOpen" title="Rate this book" size="md">
    <div class="flex flex-col gap-6">
      <div class="flex flex-col items-center gap-3">
        <p class="text-sm text-gray-500 self-start">Your rating</p>
        <div class="flex gap-2">
          <i
            v-for="i in 5"
            :key="i"
            class="pi cursor-pointer text-4xl transition-colors"
            :class="i <= (hovered || form.rating) ? 'pi-star-fill text-amber-400' : 'pi-star text-gray-300'"
            @mouseenter="hovered = i"
            @mouseleave="hovered = 0"
            @click="form.rating = i"
          />
        </div>
        <p class="text-sm text-gray-400 min-h-4.5">{{ ratingLabel }} &nbsp;</p>
      </div>

      <div class="flex flex-col gap-2">
        <label class="text-sm text-gray-500">Your review</label>
        <textarea
          v-model="form.review_text"
          maxlength="500"
          placeholder="Share your thoughts about this book..."
          class="w-full min-h-25 resize-y text-sm p-3 rounded-lg border border-gray-200 
          bg-gray-50 focus:outline-none focus:ring-2 focus:ring-emerald-500"
        />
        <p class="text-xs text-gray-400 text-right">{{ form.review_text.length }} / 200</p>
      </div>
    </div>

    <template #footer>
      <button
        class="px-4 py-2 text-sm text-gray-500 border border-gray-200 rounded-md hover:bg-gray-50"
      >
        Cancel
      </button>
      <button
        :disabled="!isValid"
        class="px-5 py-2 text-sm font-medium text-white bg-emerald-700 rounded-md 
        disabled:opacity-50 disabled:cursor-not-allowed active:bg-emerald-900 cursor-pointer"
        @click="handleSubmit"
      >
        Submit review
      </button>
    </template>
  </CommonModal>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import CommonModal from './CommonModal.vue'
import type { ReviewCreate } from '@/types/review_types';

const emit = defineEmits<{
  'submit': [data: ReviewCreate]
}>()

const isOpen = ref(false)
const hovered = ref(0)

const form = reactive({
  rating: 0,
  review_text: ''
})

const labels = ['', 'Poor', 'Fair', 'Good', 'Very good', 'Excellent']
const ratingLabel = computed(() => labels[hovered.value || form.rating] ?? '')
const isValid = computed(() => form.rating > 0 && form.review_text.trim().length > 0)

const handleSubmit = () => {
  if (!isValid.value) return
  emit('submit', form)
  form.rating = 0
  form.review_text = ''
}

const open = () => { isOpen.value = true }
const close = () => {isOpen.value = false}

defineExpose({open, close})

</script>